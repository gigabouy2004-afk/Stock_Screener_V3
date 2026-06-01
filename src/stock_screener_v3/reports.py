from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from stock_screener_v3.backtest_engine import summarize_result
from stock_screener_v3.models import BacktestResult


def write_detail_csv(result: BacktestResult, path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = list(result.detail_rows)
    if not rows:
        output.write_text("", encoding="utf-8")
        return
    fieldnames = list(dict.fromkeys(key for row in rows for key in row.keys()))
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def render_summary_markdown(result: BacktestResult) -> str:
    summary = summarize_result(result)
    lines: list[str] = [
        "# V3 Backtest Summary",
        "",
        f"- D date: {summary['d_date']}",
        f"- Universe file: {result.config.universe_file}",
        f"- Stage families: {', '.join(result.config.stage_families)}",
        f"- Sample mode: {result.config.sample_mode}",
        f"- Symbols attempted: {summary['symbols_attempted']}",
        f"- Symbols processed: {summary['symbols_processed']}",
        f"- Symbols skipped: {summary['symbols_skipped']}",
        f"- Candidates found: {summary['candidates_found']}",
        f"- Candidate density: {float(summary['candidate_density']):.4f}",
        "",
        "## Forward Outcomes",
        "",
        "| Horizon | Evaluated | Positive | Hit Rate |",
        "|---|---:|---:|---:|",
    ]
    for days in result.config.forward_days:
        evaluated = int(summary.get(f"d_plus_{days}_evaluated", 0))
        positive = int(summary.get(f"d_plus_{days}_positive", 0))
        hit_rate = float(summary.get(f"d_plus_{days}_hit_rate", 0.0))
        lines.append(f"| D+{days} | {evaluated} | {positive} | {hit_rate:.2%} |")
    if result.skip_reasons:
        lines.extend(["", "## Skip Reasons", ""])
        for reason, count in sorted(result.skip_reasons.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- {reason}: {count}")
    return "\n".join(lines) + "\n"


def write_summary_markdown(result: BacktestResult, path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_summary_markdown(result), encoding="utf-8")


def row_value(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    return "" if value is None else str(value)

