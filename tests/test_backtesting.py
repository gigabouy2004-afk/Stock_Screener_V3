from __future__ import annotations

import unittest

import pandas as pd

from stock_screener_v3.backtesting import forward_return, slice_as_of


class BacktestingUtilityTests(unittest.TestCase):
    def test_slice_as_of_excludes_future_rows(self) -> None:
        frame = pd.DataFrame(
            {"Close": [100.0, 101.0, 102.0, 103.0]},
            index=pd.to_datetime(["2026-02-10", "2026-02-11", "2026-02-12", "2026-02-13"]),
        )

        sliced = slice_as_of(frame, pd.Timestamp("2026-02-11 23:59:59"))

        self.assertEqual(list(sliced.frame["Close"]), [100.0, 101.0])
        self.assertEqual(sliced.as_of.date().isoformat(), "2026-02-11")

    def test_forward_return_uses_future_only_after_cutoff(self) -> None:
        frame = pd.DataFrame(
            {"Close": [100.0, 110.0, 121.0, 100.0]},
            index=pd.to_datetime(["2026-02-10", "2026-02-11", "2026-02-12", "2026-02-13"]),
        )

        self.assertEqual(forward_return(frame, pd.Timestamp("2026-02-11 23:59:59"), 1), 10.0)
        self.assertEqual(forward_return(frame, pd.Timestamp("2026-02-11 23:59:59"), 2), -9.0909)

    def test_forward_return_returns_none_when_horizon_missing(self) -> None:
        frame = pd.DataFrame(
            {"Close": [100.0, 110.0]},
            index=pd.to_datetime(["2026-02-10", "2026-02-11"]),
        )

        self.assertIsNone(forward_return(frame, pd.Timestamp("2026-02-11"), 1))


if __name__ == "__main__":
    unittest.main()

