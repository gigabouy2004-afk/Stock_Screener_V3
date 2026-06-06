from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

from stock_screener_v3.models import BacktestResult, BacktestRunConfig
from stock_screener_v3.output_contracts import V2_COMPAT_EXPORT_COLUMNS
from stock_screener_v3.reports import render_multi_date_summary_markdown, render_summary_markdown, write_detail_csv, write_summary_markdown


class ReportTests(unittest.TestCase):
    def test_render_summary_markdown_includes_density_and_forward_table(self) -> None:
        result = BacktestResult(
            config=BacktestRunConfig(universe_file="memory", d_date=date(2026, 2, 11), stage_families=("MOCK",), forward_days=(1,)),
            generated_at=datetime(2026, 6, 2),
            symbols_attempted=2,
            symbols_processed=2,
            symbols_skipped=0,
            candidates_found=1,
            detail_rows=(
                {
                    "Symbol": "AAA",
                    "CandidateClass": "SELECTED",
                    "StageFamily": "CROSSOVER",
                    "TotalScore": 72.0,
                    "RiskTags": "BELOW_EMA200",
                    "DPlus1ReturnPct": 2.0,
                    "DPlus1WorstLowReturnPct": -3.0,
                    "DPlus1BestHighReturnPct": 4.0,
                    "CandidateStateRaw": "PRE_BULL_CROSSOVER",
                    "RankingCandidateStates": "CROSSOVER:PRE_BULL_CROSSOVER|MOMENTUM_SETUP:STATUS_QUO|DIVERGENCE:BULLISH_DIVERGENCE",
                },
                {"Symbol": "BBB", "CandidateClass": "STATUS_QUO", "DPlus1ReturnPct": -1.0},
            ),
        )

        markdown = render_summary_markdown(result)

        self.assertIn("Candidate density: 0.5000", markdown)
        self.assertIn("| D+1 | 1 | 1 | 100.00% |", markdown)
        self.assertIn("2.00%", markdown)
        self.assertIn("## Score Buckets", markdown)
        self.assertIn("| 70-79 | 1 |", markdown)
        self.assertIn("## Score Bucket Outcomes D+1", markdown)
        self.assertIn("## Stage Family Outcomes D+1", markdown)
        self.assertIn("| CROSSOVER | 1 | 1 | 1 | 100.00% | 2.00% | 2.00% |", markdown)
        self.assertIn("## Stage Family Path Outcomes D+1", markdown)
        self.assertIn("| CROSSOVER | 1 | 1 | -3.00% | -3.00% | 4.00% | 4.00% |", markdown)
        self.assertIn("## Candidate State Path Outcomes D+1", markdown)
        self.assertIn("| PRE_BULL_CROSSOVER | 1 | 1 | -3.00% | -3.00% | 4.00% | 4.00% |", markdown)
        self.assertIn("## Sector Outcomes D+1", markdown)
        self.assertIn("## Review Priority Outcomes D+1", markdown)
        self.assertIn("## Risk Tag Outcomes D+1", markdown)
        self.assertIn("| BELOW_EMA200 | 1 | 1 | 1 | 100.00% | 2.00% | 2.00% |", markdown)
        self.assertIn("## Ranking Collision Buckets", markdown)
        self.assertIn("| CROSSOVER+DIVERGENCE | 1 |", markdown)

    def test_render_summary_markdown_includes_failure_categories(self) -> None:
        result = BacktestResult(
            config=BacktestRunConfig(universe_file="memory", d_date=date(2026, 2, 11), stage_families=("MOCK",), forward_days=(1,)),
            generated_at=datetime(2026, 6, 2),
            symbols_attempted=1,
            symbols_processed=1,
            symbols_skipped=0,
            candidates_found=1,
            detail_rows=(
                {
                    "Symbol": "AAA",
                    "CandidateClass": "SELECTED",
                    "TotalScore": 65.0,
                    "FailureCategory": "PARTICIPATION_FAILURE",
                    "DPlus1ReturnPct": -2.0,
                },
            ),
        )

        markdown = render_summary_markdown(result)

        self.assertIn("## Failure Categories", markdown)
        self.assertIn("- PARTICIPATION_FAILURE: 1", markdown)

    def test_render_multi_date_summary_markdown_includes_aggregate_metrics(self) -> None:
        first = BacktestResult(
            config=BacktestRunConfig(universe_file="memory", d_date=date(2026, 2, 11), stage_families=("MOCK",), forward_days=(1,)),
            generated_at=datetime(2026, 6, 2),
            symbols_attempted=1,
            symbols_processed=1,
            symbols_skipped=0,
            candidates_found=1,
            detail_rows=(
                {
                    "Symbol": "AAA",
                    "CandidateClass": "SELECTED",
                    "StageFamily": "CROSSOVER",
                    "CandidateStateRaw": "PRE_BEAR_CROSSOVER",
                    "DPlus1ReturnPct": 2.0,
                    "DPlus1WorstLowReturnPct": -4.0,
                    "DPlus1BestHighReturnPct": 5.0,
                    "RankingCandidateStates": "CROSSOVER:PRE_BULL_CROSSOVER|MOMENTUM_SETUP:STATUS_QUO",
                },
            ),
        )
        second = BacktestResult(
            config=BacktestRunConfig(universe_file="memory", d_date=date(2026, 3, 11), stage_families=("MOCK",), forward_days=(1,)),
            generated_at=datetime(2026, 6, 2),
            symbols_attempted=1,
            symbols_processed=1,
            symbols_skipped=0,
            candidates_found=1,
            detail_rows=(
                {
                    "Symbol": "BBB",
                    "CandidateClass": "WATCH",
                    "StageFamily": "MOMENTUM_SETUP",
                    "CandidateStateRaw": "BULL_PULLBACK_REENTRY",
                    "DPlus1ReturnPct": -1.0,
                    "DPlus1WorstLowReturnPct": -6.0,
                    "DPlus1BestHighReturnPct": 1.0,
                    "RankingCandidateStates": "CROSSOVER:STATUS_QUO|MOMENTUM_SETUP:BULL_PULLBACK_REENTRY",
                },
            ),
        )

        markdown = render_multi_date_summary_markdown((first, second))

        self.assertIn("# V3 Multi-Date Backtest Summary", markdown)
        self.assertIn("| 2026-02-11 | 1 | 0 | 1 | 1.0000 |", markdown)
        self.assertIn("| D+1 | 2 | 1 | 50.00% | 0.50% | 0.50% |", markdown)
        self.assertIn("## Aggregate Forward Path Outcomes", markdown)
        self.assertIn("| D+1 | 2 | -5.00% | -5.00% | 3.00% | 3.00% |", markdown)
        self.assertIn("## Stage Family Path Outcomes D+1", markdown)
        self.assertIn("| CROSSOVER | 1 | 1 | -4.00% | -4.00% | 5.00% | 5.00% |", markdown)
        self.assertIn("| MOMENTUM_SETUP | 1 | 1 | -6.00% | -6.00% | 1.00% | 1.00% |", markdown)
        self.assertIn("## Candidate State Path Outcomes D+1", markdown)
        self.assertIn("| PRE_BEAR_CROSSOVER | 1 | 1 | -4.00% | -4.00% | 5.00% | 5.00% |", markdown)
        self.assertIn("## Ranking Collision Buckets", markdown)
        self.assertIn("| CROSSOVER | 1 |", markdown)
        self.assertIn("| MOMENTUM_SETUP | 1 |", markdown)

    def test_write_reports_creates_files(self) -> None:
        result = BacktestResult(
            config=BacktestRunConfig(universe_file="memory", d_date=date(2026, 2, 11), stage_families=("MOCK",), forward_days=(1,)),
            generated_at=datetime(2026, 6, 2),
            symbols_attempted=1,
            symbols_processed=1,
            symbols_skipped=0,
            candidates_found=1,
            detail_rows=({"Symbol": "AAA", "CandidateClass": "SELECTED", "DPlus1ReturnPct": 2.0},),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            detail = Path(tmpdir) / "details.csv"
            summary = Path(tmpdir) / "summary.md"

            write_detail_csv(result, detail)
            write_summary_markdown(result, summary)

            self.assertIn("Symbol", detail.read_text(encoding="utf-8"))
            self.assertIn("V3 Backtest Summary", summary.read_text(encoding="utf-8"))

    def test_detail_csv_preserves_v2_compatible_header_order(self) -> None:
        result = BacktestResult(
            config=BacktestRunConfig(universe_file="memory", d_date=date(2026, 2, 11), stage_families=("MOCK",)),
            generated_at=datetime(2026, 6, 2),
            symbols_attempted=1,
            symbols_processed=1,
            symbols_skipped=0,
            candidates_found=1,
            detail_rows=({"Symbol": "AAA", "CandidateClass": "SELECTED", "CustomDiagnostic": "kept"},),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            detail = Path(tmpdir) / "details.csv"

            write_detail_csv(result, detail)

            header = detail.read_text(encoding="utf-8").splitlines()[0].split(",")
            self.assertEqual(V2_COMPAT_EXPORT_COLUMNS, header[: len(V2_COMPAT_EXPORT_COLUMNS)])
            self.assertIn("CandidateClass", header)
            self.assertIn("CustomDiagnostic", header)

    def test_detail_csv_writes_headers_even_when_no_rows(self) -> None:
        result = BacktestResult(
            config=BacktestRunConfig(universe_file="memory", d_date=date(2026, 2, 11), stage_families=("MOCK",)),
            generated_at=datetime(2026, 6, 2),
            symbols_attempted=1,
            symbols_processed=1,
            symbols_skipped=0,
            candidates_found=0,
            detail_rows=(),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            detail = Path(tmpdir) / "empty.csv"

            write_detail_csv(result, detail)

            header = detail.read_text(encoding="utf-8").splitlines()[0].split(",")
            self.assertEqual(V2_COMPAT_EXPORT_COLUMNS, header[: len(V2_COMPAT_EXPORT_COLUMNS)])


if __name__ == "__main__":
    unittest.main()
