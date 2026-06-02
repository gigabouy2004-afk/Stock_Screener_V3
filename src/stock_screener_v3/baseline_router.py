from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import pandas as pd

from stock_screener_v3.indicators import ema, latest_number, macd
from stock_screener_v3.models import CandidateClass, EvidencePack, ReviewPriority, ScoreResult, StageEvaluation


class Regime(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class BaselineDecision:
    market_regime: Regime
    sector_regime: Regime
    stock_regime: Regime
    allow_bullish: bool
    allow_bearish: bool
    blocked_stage_families: tuple[str, ...]
    reason: str

    def to_diagnostics(self) -> dict[str, object]:
        return {
            "MarketRegime": self.market_regime.value,
            "SectorRegime": self.sector_regime.value,
            "StockRegime": self.stock_regime.value,
            "AllowedBullishStages": self.allow_bullish,
            "AllowedBearishStages": self.allow_bearish,
            "BlockedStageFamilies": ",".join(self.blocked_stage_families),
            "BaselineRouteReason": self.reason,
        }


def build_baseline_decision(evidence: EvidencePack) -> BaselineDecision:
    market_regime = Regime(str(evidence.market_context.get("MarketRegime") or Regime.UNKNOWN))
    sector_regime = Regime(str(evidence.sector_context.get("SectorRegime") or Regime.UNKNOWN))
    stock_regime = classify_stock_regime(evidence)

    blocked: list[str] = []
    allow_bullish = True
    allow_bearish = True
    reason = "BASELINE_CONTEXT_ALLOWS_SELECTED_FAMILIES"

    if market_regime == Regime.BEARISH and sector_regime == Regime.BEARISH and stock_regime == Regime.BEARISH:
        allow_bullish = False
        blocked.append("BULLISH_ENTRY")
        blocked.append("MOMENTUM_SETUP")
        reason = "MARKET_SECTOR_STOCK_ALL_BEARISH_BLOCK_BULLISH_ENTRY"
    elif market_regime == Regime.BEARISH and sector_regime == Regime.BEARISH and stock_regime == Regime.MIXED:
        blocked.append("MOMENTUM_SETUP")
        reason = "BEARISH_MARKET_AND_SECTOR_LIMIT_BULLISH_ENTRY_TO_WATCH"
    elif stock_regime == Regime.BEARISH:
        blocked.append("MOMENTUM_SETUP")
        reason = "BEARISH_STOCK_BASELINE_BLOCKS_MOMENTUM_SETUP"

    return BaselineDecision(
        market_regime=market_regime,
        sector_regime=sector_regime,
        stock_regime=stock_regime,
        allow_bullish=allow_bullish,
        allow_bearish=allow_bearish,
        blocked_stage_families=tuple(blocked),
        reason=reason,
    )


def classify_stock_regime(evidence: EvidencePack) -> Regime:
    price = _number(evidence.stock_baseline.get("LatestPrice"))
    ema20_value = _number(evidence.trend.get("EMA20"))
    ema50_value = _number(evidence.trend.get("EMA50"))
    ema200_value = _number(evidence.trend.get("EMA200"))
    macd_state = str(evidence.momentum.get("MACD_1D_State") or "")
    histogram_improving = bool(evidence.momentum.get("MACDHistogramImproving"))
    plus_di = _number(evidence.trend.get("PlusDI_1D"))
    minus_di = _number(evidence.trend.get("MinusDI_1D"))

    bullish_points = 0
    bearish_points = 0
    if price is not None and ema20_value is not None:
        bullish_points += int(price >= ema20_value)
        bearish_points += int(price < ema20_value)
    if price is not None and ema50_value is not None:
        bullish_points += int(price >= ema50_value)
        bearish_points += int(price < ema50_value)
    if price is not None and ema200_value is not None:
        bullish_points += int(price >= ema200_value)
        bearish_points += int(price < ema200_value)
    if macd_state == "BULLISH":
        bullish_points += 1
    elif macd_state == "BEARISH":
        bearish_points += 1
    if histogram_improving:
        bullish_points += 1
    else:
        bearish_points += 1
    if plus_di is not None and minus_di is not None:
        bullish_points += int(plus_di >= minus_di)
        bearish_points += int(minus_di > plus_di)

    if bullish_points >= 5 and bearish_points <= 1:
        return Regime.BULLISH
    if bearish_points >= 5 and bullish_points <= 1:
        return Regime.BEARISH
    if bullish_points or bearish_points:
        return Regime.MIXED
    return Regime.UNKNOWN


def classify_benchmark_regime(frame: pd.DataFrame | None) -> Regime:
    if frame is None or frame.empty or "Close" not in frame.columns:
        return Regime.UNKNOWN
    close = pd.to_numeric(frame["Close"], errors="coerce").dropna()
    if len(close) < 60:
        return Regime.UNKNOWN
    ema50_value = latest_number(ema(close, 50))
    ema200_value = latest_number(ema(close, 200))
    latest_close = latest_number(close)
    macd_frame = macd(close)
    latest_histogram = latest_number(macd_frame["Histogram"])
    previous_histogram = _previous_number(macd_frame["Histogram"])

    bullish = 0
    bearish = 0
    if latest_close is not None and ema50_value is not None:
        bullish += int(latest_close >= ema50_value)
        bearish += int(latest_close < ema50_value)
    if latest_close is not None and ema200_value is not None:
        bullish += int(latest_close >= ema200_value)
        bearish += int(latest_close < ema200_value)
    if latest_histogram is not None and latest_histogram >= 0:
        bullish += 1
    elif latest_histogram is not None:
        bearish += 1
    if previous_histogram is not None and latest_histogram is not None and latest_histogram >= previous_histogram:
        bullish += 1
    elif previous_histogram is not None and latest_histogram is not None:
        bearish += 1

    if bullish >= 3 and bearish <= 1:
        return Regime.BULLISH
    if bearish >= 3 and bullish <= 1:
        return Regime.BEARISH
    return Regime.MIXED


def apply_baseline_decision(evaluation: StageEvaluation, decision: BaselineDecision) -> StageEvaluation:
    direction = str(
        evaluation.diagnostics.get("CrossoverDirection")
        or evaluation.diagnostics.get("MomentumSetupDirection")
        or "NONE"
    )
    if direction == "BULLISH" and not decision.allow_bullish:
        diagnostics = dict(evaluation.diagnostics)
        diagnostics.update(decision.to_diagnostics())
        diagnostics["BaselineBlockedOriginalState"] = evaluation.candidate_state
        diagnostics["CandidateStateRaw"] = "STATUS_QUO"
        return StageEvaluation(
            symbol=evaluation.symbol,
            candidate_state="STATUS_QUO",
            candidate_class=CandidateClass.STATUS_QUO,
            review_priority=ReviewPriority.NONE,
            confidence="LOW",
            score=ScoreResult(total_score=0.0, labels=("BASELINE_BLOCKED_BULLISH_ENTRY",)),
            reason_codes=("BASELINE_BLOCKED_BULLISH_ENTRY",),
            risk_tags=evaluation.risk_tags,
            diagnostics=diagnostics,
        )
    diagnostics = dict(evaluation.diagnostics)
    diagnostics.update(decision.to_diagnostics())
    return StageEvaluation(
        symbol=evaluation.symbol,
        candidate_state=evaluation.candidate_state,
        candidate_class=evaluation.candidate_class,
        review_priority=evaluation.review_priority,
        confidence=evaluation.confidence,
        score=evaluation.score,
        reason_codes=evaluation.reason_codes,
        risk_tags=evaluation.risk_tags,
        diagnostics=diagnostics,
    )


def _number(value: object) -> float | None:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def _previous_number(series: pd.Series) -> float | None:
    cleaned = pd.to_numeric(series, errors="coerce").dropna()
    if len(cleaned) < 2:
        return None
    return round(float(cleaned.iloc[-2]), 4)
