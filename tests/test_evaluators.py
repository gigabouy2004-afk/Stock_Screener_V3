from __future__ import annotations

import unittest

import pandas as pd

from stock_screener_v3.evaluators import CrossoverEvaluator, evaluate_crossover
from stock_screener_v3.models import CandidateClass, EvidencePack, PriceDataBundle, UniverseRecord


def make_price_frame(values: list[float]) -> pd.DataFrame:
    index = pd.date_range("2025-10-01", periods=len(values), freq="B")
    close = pd.Series(values, index=index)
    return pd.DataFrame(
        {
            "Open": close.shift(1).fillna(close.iloc[0]),
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": [250_000 + index_ * 1_000 for index_ in range(len(values))],
        },
        index=index,
    )


class CrossoverEvaluatorTests(unittest.TestCase):
    def test_crossover_evaluator_selects_constructive_bull_transition(self) -> None:
        values = [100 - index * 0.12 for index in range(45)] + [95 + index * 0.55 for index in range(55)]
        record = UniverseRecord(symbol="AAA", yahoo_symbol="AAA", sector="Technology", exchange="NASDAQ")
        prices = PriceDataBundle(symbol="AAA", daily=make_price_frame(values))

        evaluation = CrossoverEvaluator().evaluate(record, prices)

        self.assertIn(evaluation.candidate_class, {CandidateClass.SELECTED, CandidateClass.WATCH})
        self.assertIn(evaluation.candidate_state, {"PRE_BULL_CROSSOVER", "BULL_PULLBACK_REENTRY", "BULL_CONTINUATION_MOMENTUM"})
        self.assertIn("MACD_1D_CrossoverState", evaluation.diagnostics)
        self.assertIn("CrossoverOpportunityType", evaluation.diagnostics)
        self.assertIn("CrossoverQualityComponents", evaluation.diagnostics)

    def test_crossover_evaluator_returns_status_quo_without_route(self) -> None:
        values = [100 - index * 0.4 for index in range(100)]
        record = UniverseRecord(symbol="BBB", yahoo_symbol="BBB", sector="Energy", exchange="NYSE")
        prices = PriceDataBundle(symbol="BBB", daily=make_price_frame(values))

        evaluation = CrossoverEvaluator().evaluate(record, prices)

        self.assertEqual(evaluation.candidate_class, CandidateClass.STATUS_QUO)
        self.assertEqual(evaluation.candidate_state, "STATUS_QUO")
        self.assertIn("NO_CROSSOVER_ROUTE", evaluation.reason_codes)

    def test_crossover_evaluator_classifies_bull_pullback_reentry(self) -> None:
        evaluation = evaluate_crossover(
            make_evidence(
                structure={"EMA20_Reclaim": True, "HigherLow_5D": False, "PriceLadder_Passed": True},
            )
        )

        self.assertEqual(evaluation.candidate_state, "BULL_PULLBACK_REENTRY")
        self.assertEqual(evaluation.diagnostics["CrossoverOpportunityType"], "BULLISH_PULLBACK_REENTRY")
        self.assertIn("BULL_PULLBACK_REENTRY_ROUTE", evaluation.reason_codes)

    def test_crossover_evaluator_classifies_bull_continuation(self) -> None:
        evaluation = evaluate_crossover(
            make_evidence(
                structure={"EMA20_Reclaim": False, "HigherLow_5D": False, "PriceLadder_Passed": True},
            )
        )

        self.assertEqual(evaluation.candidate_state, "BULL_CONTINUATION_MOMENTUM")
        self.assertEqual(evaluation.diagnostics["CrossoverOpportunityType"], "BULLISH_CONTINUATION_MOMENTUM")
        self.assertIn("BULL_CONTINUATION_ROUTE", evaluation.reason_codes)


def make_evidence(structure: dict[str, object]) -> EvidencePack:
    return EvidencePack(
        record=UniverseRecord(symbol="AAA", yahoo_symbol="AAA", sector="Technology", exchange="NASDAQ"),
        as_of=pd.Timestamp("2026-02-11"),
        stock_baseline={"LatestPrice": 105.0, "DailyCloseLocationPct": 72.0},
        momentum={
            "RSI_1D": 56.0,
            "MACD_1D_CrossoverState": "ABOVE_SIGNAL",
            "MACD_1D_Histogram": 0.2,
            "MACD_1D_CrossoverDistance": 0.2,
            "MACDHistogramImproving": True,
        },
        trend={
            "EMA20": 100.0,
            "EMA50": 96.0,
            "EMA200": 90.0,
            "ADX_1D": 24.0,
            "PlusDI_1D": 28.0,
            "MinusDI_1D": 16.0,
        },
        volume={"IntradayVolumeVs20Avg": 130.0},
        structure=structure,
        risk_context={"LowLiquidity": False, "BelowEMA200": False},
    )


if __name__ == "__main__":
    unittest.main()
