from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import tempfile
import unittest

from stock_screener_v3.models import BacktestResult, BacktestRunConfig
from stock_screener_v3.reports import render_summary_markdown, write_detail_csv, write_summary_markdown


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
                {"Symbol": "AAA", "CandidateClass": "SELECTED", "DPlus1ReturnPct": 2.0},
                {"Symbol": "BBB", "CandidateClass": "STATUS_QUO", "DPlus1ReturnPct": -1.0},
            ),
        )

        markdown = render_summary_markdown(result)

        self.assertIn("Candidate density: 0.5000", markdown)
        self.assertIn("| D+1 | 1 | 1 | 100.00% |", markdown)

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


if __name__ == "__main__":
    unittest.main()

