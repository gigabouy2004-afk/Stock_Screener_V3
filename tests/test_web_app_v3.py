from __future__ import annotations

import unittest

import web_app_v3


class WebAppV3RenderTests(unittest.TestCase):
    def test_results_table_marks_bear_crossover_as_exit_review(self) -> None:
        html = web_app_v3.render_results_table(
            (
                {
                    "Symbol": "AAA",
                    "CandidateState": "PRE_BEAR_CROSSOVER",
                    "CandidateClass": "SELECTED",
                    "StageFamily": "CROSSOVER",
                    "TotalScore": "81.0",
                },
            )
        )

        self.assertIn("ReviewIntent", html)
        self.assertIn("Exit / preservation", html)
        self.assertIn('class="row-exit"', html)
        self.assertIn('class="chip exit"', html)

    def test_review_split_counts_entry_exit_and_bear_risk_separately(self) -> None:
        html = web_app_v3.render_review_split(
            (
                {"CandidateState": "PRE_BULL_CROSSOVER"},
                {"CandidateState": "PRE_BEAR_CROSSOVER"},
                {"CandidateState": "BEARISH_DIVERGENCE"},
            )
        )

        self.assertIn("Bullish entry / re-entry", html)
        self.assertIn("Exit / preservation", html)
        self.assertIn("Bearish risk review", html)
        self.assertIn('<div class="intent-card entry"><span class="intent-count">1</span>', html)
        self.assertIn('<div class="intent-card exit"><span class="intent-count">1</span>', html)
        self.assertIn('<div class="intent-card bear"><span class="intent-count">1</span>', html)


if __name__ == "__main__":
    unittest.main()
