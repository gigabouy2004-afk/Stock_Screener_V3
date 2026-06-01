from __future__ import annotations

from dataclasses import dataclass

from stock_screener_v3.evidence import EvidenceBuilder, evidence_to_diagnostics
from stock_screener_v3.models import (
    CandidateClass,
    EvidencePack,
    PriceDataBundle,
    ReviewPriority,
    ScoreResult,
    StageEvaluation,
    UniverseRecord,
)


@dataclass(frozen=True)
class CrossoverEvaluator:
    evidence_builder: EvidenceBuilder = EvidenceBuilder()

    def evaluate(self, record: UniverseRecord, prices: PriceDataBundle) -> StageEvaluation:
        evidence = self.evidence_builder.build(record, prices)
        return evaluate_crossover(evidence)


def evaluate_crossover(evidence: EvidencePack) -> StageEvaluation:
    diagnostics = evidence_to_diagnostics(evidence)
    momentum = evidence.momentum
    trend = evidence.trend
    volume = evidence.volume
    structure = evidence.structure
    risk = evidence.risk_context

    crossover_state = str(momentum.get("MACD_1D_CrossoverState") or "UNKNOWN")
    macd_distance = _number(momentum.get("MACD_1D_CrossoverDistance"))
    histogram = _number(momentum.get("MACD_1D_Histogram"))
    rsi = _number(momentum.get("RSI_1D"))
    close_location = _number(evidence.stock_baseline.get("DailyCloseLocationPct"))
    volume_vs_20 = _number(volume.get("IntradayVolumeVs20Avg"))
    latest_price = _number(evidence.stock_baseline.get("LatestPrice"))
    ema20 = _number(trend.get("EMA20"))
    ema200 = _number(trend.get("EMA200"))
    plus_di = _number(trend.get("PlusDI_1D"))
    minus_di = _number(trend.get("MinusDI_1D"))

    histogram_improving = bool(momentum.get("MACDHistogramImproving"))
    route_score = _route_score(crossover_state, macd_distance, histogram, histogram_improving)
    timing_score = _timing_score(crossover_state, momentum.get("MACDHistogramImproving"))
    structure_score = _structure_score(latest_price, ema20, ema200, bool(structure.get("HigherLow_5D")))
    participation_score = _participation_score(volume_vs_20, plus_di, minus_di)
    context_score = _context_score(rsi, close_location)
    risk_score = _risk_score(bool(risk.get("LowLiquidity")), bool(risk.get("BelowEMA200")))
    total = round(route_score + timing_score + structure_score + participation_score + context_score + risk_score, 2)

    reason_codes: list[str] = []
    risk_tags: list[str] = []
    if crossover_state == "BULL_CROSS":
        reason_codes.append("DAILY_MACD_BULL_CROSS")
    elif crossover_state == "ABOVE_SIGNAL" and histogram_improving:
        reason_codes.append("DAILY_MACD_ABOVE_SIGNAL_IMPROVING")
    elif macd_distance is not None and macd_distance < 0 and histogram_improving:
        reason_codes.append("DAILY_MACD_NEAR_BULL_TRANSITION")
    else:
        reason_codes.append("NO_CROSSOVER_ROUTE")

    if structure_score >= 14:
        reason_codes.append("CONSTRUCTIVE_PRICE_STRUCTURE")
    if participation_score >= 10:
        reason_codes.append("PARTICIPATION_SUPPORT")
    if context_score >= 8:
        reason_codes.append("ACCEPTANCE_SUPPORT")
    if risk.get("LowLiquidity"):
        risk_tags.append("LOW_LIQUIDITY")
    if risk.get("BelowEMA200"):
        risk_tags.append("BELOW_EMA200")

    route_valid = route_score >= 15
    if not route_valid:
        candidate_state = "STATUS_QUO"
        candidate_class = CandidateClass.STATUS_QUO
        priority = ReviewPriority.NONE
        confidence = "LOW"
    elif total >= 72 and not risk_tags:
        candidate_state = "PRE_BULL_CROSSOVER"
        candidate_class = CandidateClass.SELECTED
        priority = ReviewPriority.A
        confidence = "HIGH"
    elif total >= 58:
        candidate_state = "PRE_BULL_CROSSOVER"
        candidate_class = CandidateClass.WATCH
        priority = ReviewPriority.B if not risk_tags else ReviewPriority.NEEDS_MANUAL_REVIEW
        confidence = "MEDIUM"
    else:
        candidate_state = "PRE_BULL_CROSSOVER"
        candidate_class = CandidateClass.REJECTED
        priority = ReviewPriority.C
        confidence = "LOW"

    diagnostics.update(
        {
            "CandidateStateRaw": candidate_state,
            "WeightedScore": total if candidate_class != CandidateClass.STATUS_QUO else None,
            "MACDScore": route_score + timing_score,
            "RSIScore": _rsi_score(rsi),
            "ADXScore": _adx_score(_number(trend.get("ADX_1D"))),
            "ScoreWeights": "route=30,structure=20,participation=15,acceptance=15,context=10,risk=10",
            "ConfirmationScore": round(timing_score + structure_score + participation_score, 2),
            "QualityContextScore": round(context_score + risk_score, 2),
            "CrossoverInternalState": crossover_state,
            "CrossoverConfidence": confidence,
            "CrossoverQualityScore": total,
            "CrossoverQualityComponents": (
                f"route={route_score};timing={timing_score};structure={structure_score};"
                f"participation={participation_score};context={context_score};risk={risk_score}"
            ),
            "CrossoverTimingProfile": "fresh" if crossover_state == "BULL_CROSS" else "developing",
            "CrossoverReason": "; ".join(reason_codes),
            "CrossoverReasonCodes": ",".join(reason_codes),
            "SetupPassed": candidate_class in {CandidateClass.SELECTED, CandidateClass.WATCH},
            "SetupScore": total,
        }
    )

    return StageEvaluation(
        symbol=evidence.record.yahoo_symbol,
        candidate_state=candidate_state,
        candidate_class=candidate_class,
        review_priority=priority,
        confidence=confidence,
        score=ScoreResult(
            total_score=total,
            route_score=route_score,
            timing_score=timing_score,
            structure_score=structure_score,
            participation_score=participation_score,
            context_score=context_score,
            risk_score=risk_score,
            labels=tuple(reason_codes),
        ),
        reason_codes=tuple(reason_codes),
        risk_tags=tuple(risk_tags),
        diagnostics=diagnostics,
    )


def _route_score(
    crossover_state: str,
    macd_distance: float | None,
    histogram: float | None,
    histogram_improving: bool,
) -> float:
    if crossover_state == "BULL_CROSS":
        return 30.0
    if crossover_state == "ABOVE_SIGNAL":
        return 24.0
    if histogram_improving and macd_distance is not None and histogram is not None and macd_distance > -0.15 and histogram > -0.15:
        return 18.0
    return 0.0


def _timing_score(crossover_state: str, improving: object) -> float:
    score = 0.0
    if crossover_state == "BULL_CROSS":
        score += 10.0
    if bool(improving):
        score += 10.0
    return min(score, 20.0)


def _structure_score(price: float | None, ema20: float | None, ema200: float | None, higher_low: bool) -> float:
    score = 0.0
    if price is not None and ema20 is not None and price >= ema20:
        score += 8.0
    if price is not None and ema200 is not None and price >= ema200:
        score += 7.0
    if higher_low:
        score += 5.0
    return score


def _participation_score(volume_vs_20: float | None, plus_di: float | None, minus_di: float | None) -> float:
    score = 0.0
    if volume_vs_20 is not None and volume_vs_20 >= 100:
        score += 8.0
    if plus_di is not None and minus_di is not None and plus_di >= minus_di:
        score += 7.0
    return score


def _context_score(rsi: float | None, close_location: float | None) -> float:
    score = 0.0
    if rsi is not None and 45 <= rsi <= 70:
        score += 5.0
    if close_location is not None and close_location >= 60:
        score += 5.0
    return score


def _risk_score(low_liquidity: bool, below_ema200: bool) -> float:
    score = 10.0
    if low_liquidity:
        score -= 5.0
    if below_ema200:
        score -= 5.0
    return max(score, 0.0)


def _rsi_score(rsi: float | None) -> float:
    if rsi is None:
        return 0.0
    if 50 <= rsi <= 65:
        return 10.0
    if 45 <= rsi < 50 or 65 < rsi <= 72:
        return 6.0
    return 2.0


def _adx_score(adx_value: float | None) -> float:
    if adx_value is None:
        return 0.0
    if adx_value >= 25:
        return 10.0
    if adx_value >= 18:
        return 6.0
    return 2.0


def _number(value: object) -> float | None:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None
