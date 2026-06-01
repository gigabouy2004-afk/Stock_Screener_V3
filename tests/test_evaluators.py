from __future__ import annotations

import unittest

import pandas as pd

from stock_screener_v3.evaluators import CrossoverEvaluator
from stock_screener_v3.models import CandidateClass, PriceDataBundle, UniverseRecord


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
        self.assertEqual(evaluation.candidate_state, "PRE_BULL_CROSSOVER")
        self.assertIn("MACD_1D_CrossoverState", evaluation.diagnostics)
        self.assertIn("CrossoverQualityComponents", evaluation.diagnostics)

    def test_crossover_evaluator_returns_status_quo_without_route(self) -> None:
        values = [100 - index * 0.4 for index in range(100)]
        record = UniverseRecord(symbol="BBB", yahoo_symbol="BBB", sector="Energy", exchange="NYSE")
        prices = PriceDataBundle(symbol="BBB", daily=make_price_frame(values))

        evaluation = CrossoverEvaluator().evaluate(record, prices)

        self.assertEqual(evaluation.candidate_class, CandidateClass.STATUS_QUO)
        self.assertEqual(evaluation.candidate_state, "STATUS_QUO")
        self.assertIn("NO_CROSSOVER_ROUTE", evaluation.reason_codes)


if __name__ == "__main__":
    unittest.main()

