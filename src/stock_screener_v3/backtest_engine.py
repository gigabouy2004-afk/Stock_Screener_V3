from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Protocol

import pandas as pd

from stock_screener_v3.backtesting import forward_return, slice_as_of
from stock_screener_v3.models import (
    BacktestResult,
    BacktestRunConfig,
    CandidateClass,
    PriceDataBundle,
    StageEvaluation,
    UniverseRecord,
)
from stock_screener_v3.universe import deterministic_sample, filter_records


class PriceProvider(Protocol):
    def daily(self, symbol: str) -> pd.DataFrame:
        """Return daily OHLCV data for the symbol."""


class StageEvaluator(Protocol):
    def evaluate(self, record: UniverseRecord, prices: PriceDataBundle) -> StageEvaluation:
        """Evaluate one symbol using as-of price data only."""


class InMemoryPriceProvider:
    def __init__(self, frames: dict[str, pd.DataFrame]):
        self.frames = frames

    def daily(self, symbol: str) -> pd.DataFrame:
        try:
            return self.frames[symbol]
        except KeyError as exc:
            raise ValueError(f"No daily data for {symbol}.") from exc


class BacktestEngine:
    def __init__(self, price_provider: PriceProvider, evaluator: StageEvaluator):
        self.price_provider = price_provider
        self.evaluator = evaluator

    def run(self, records: list[UniverseRecord], config: BacktestRunConfig) -> BacktestResult:
        selected_records = filter_records(
            records,
            sectors=config.sector_filters,
            exchanges=config.exchange_filters,
        )
        selected_records = deterministic_sample(
            selected_records,
            sample_size=config.sample_size,
            random_seed=config.random_seed,
        )
        detail_rows: list[dict[str, object]] = []
        skip_reasons: Counter[str] = Counter()
        processed = 0
        candidates = 0
        cutoff = pd.Timestamp(config.d_date) + pd.Timedelta(hours=23, minutes=59, seconds=59)

        for record in selected_records:
            try:
                full_daily = self.price_provider.daily(record.yahoo_symbol)
                historical = slice_as_of(full_daily, cutoff)
                bundle = PriceDataBundle(
                    symbol=record.yahoo_symbol,
                    daily=historical.frame,
                    as_of=historical.as_of,
                    provider=type(self.price_provider).__name__,
                )
                evaluation = self.evaluator.evaluate(record, bundle)
                processed += 1
                is_candidate = evaluation.candidate_class in {CandidateClass.SELECTED, CandidateClass.WATCH}
                if is_candidate:
                    candidates += 1
                row = self._detail_row(record, evaluation, full_daily, cutoff, config.forward_days)
                detail_rows.append(row)
            except Exception as exc:
                skip_reasons[str(exc)] += 1

        return BacktestResult(
            config=config,
            generated_at=datetime.now(),
            symbols_attempted=len(selected_records),
            symbols_processed=processed,
            symbols_skipped=sum(skip_reasons.values()),
            candidates_found=candidates,
            detail_rows=tuple(detail_rows),
            skip_reasons=dict(skip_reasons),
        )

    @staticmethod
    def _detail_row(
        record: UniverseRecord,
        evaluation: StageEvaluation,
        full_daily: pd.DataFrame,
        cutoff: pd.Timestamp,
        forward_days: tuple[int, ...],
    ) -> dict[str, object]:
        row: dict[str, object] = {
            "Symbol": record.symbol,
            "YahooSymbol": record.yahoo_symbol,
            "CompanyName": record.company_name,
            "Exchange": record.exchange,
            "Sector": record.sector,
            "Industry": record.industry,
            "CandidateState": evaluation.candidate_state,
            "CandidateClass": evaluation.candidate_class.value,
            "ReviewPriority": evaluation.review_priority.value,
            "Confidence": evaluation.confidence,
            "TotalScore": evaluation.score.total_score,
            "RouteScore": evaluation.score.route_score,
            "TimingScore": evaluation.score.timing_score,
            "StructureScore": evaluation.score.structure_score,
            "ParticipationScore": evaluation.score.participation_score,
            "ContextScore": evaluation.score.context_score,
            "RiskScore": evaluation.score.risk_score,
            "ReasonCodes": ",".join(evaluation.reason_codes),
            "RiskTags": ",".join(evaluation.risk_tags),
        }
        row.update(evaluation.diagnostics)
        for days in forward_days:
            row[f"DPlus{days}ReturnPct"] = forward_return(full_daily, cutoff, days)
        return row


def summarize_result(result: BacktestResult) -> dict[str, object]:
    detail_rows = [
        row
        for row in result.detail_rows
        if row.get("CandidateClass") in {CandidateClass.SELECTED.value, CandidateClass.WATCH.value}
    ]
    summary = result.summary_dict()
    for days in result.config.forward_days:
        key = f"DPlus{days}ReturnPct"
        values = [row.get(key) for row in detail_rows if row.get(key) is not None]
        positive = [value for value in values if float(value) > 0]
        summary[f"d_plus_{days}_evaluated"] = len(values)
        summary[f"d_plus_{days}_positive"] = len(positive)
        summary[f"d_plus_{days}_hit_rate"] = len(positive) / len(values) if values else 0.0
    return summary
