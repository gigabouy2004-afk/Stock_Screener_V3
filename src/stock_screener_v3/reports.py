from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from stock_screener_v3.backtest_engine import summarize_result
from stock_screener_v3.models import BacktestResult
from stock_screener_v3.output_contracts import DEFAULT_DETAIL_CSV_COLUMNS


def write_detail_csv(result: BacktestResult, path: str | Path, columns: list[str] | None = None) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = list(result.detail_rows)
    base_columns = list(columns or DEFAULT_DETAIL_CSV_COLUMNS)
    fieldnames = list(dict.fromkeys(base_columns + [key for row in rows for key in row.keys()]))
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
        "| Horizon | Evaluated | Positive | Hit Rate | Average Return | Median Return |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for days in result.config.forward_days:
        evaluated = int(summary.get(f"d_plus_{days}_evaluated", 0))
        positive = int(summary.get(f"d_plus_{days}_positive", 0))
        hit_rate = float(summary.get(f"d_plus_{days}_hit_rate", 0.0))
        average_return = _format_pct_value(summary.get(f"d_plus_{days}_average_return_pct"))
        median_return = _format_pct_value(summary.get(f"d_plus_{days}_median_return_pct"))
        lines.append(f"| D+{days} | {evaluated} | {positive} | {hit_rate:.2%} | {average_return} | {median_return} |")
    score_buckets = summary.get("score_buckets", {})
    if score_buckets:
        lines.extend(["", "## Score Buckets", "", "| Bucket | Candidates |", "|---|---:|"])
        for bucket in ["80+", "70-79", "60-69", "50-59", "<50"]:
            count = int(score_buckets.get(bucket, 0))  # type: ignore[union-attr]
            if count:
                lines.append(f"| {bucket} | {count} |")
    _append_group_outcomes(
        lines,
        "Score Bucket Outcomes",
        summary.get("score_bucket_outcomes", {}),
        result.config.forward_days,
        group_order=("80+", "70-79", "60-69", "50-59", "<50"),
    )
    _append_group_outcomes(lines, "Sector Outcomes", summary.get("sector_outcomes", {}), result.config.forward_days)
    _append_group_outcomes(lines, "Review Priority Outcomes", summary.get("review_priority_outcomes", {}), result.config.forward_days)
    failure_categories = summary.get("failure_categories", {})
    if failure_categories:
        lines.extend(["", "## Failure Categories", ""])
        for category, count in sorted(failure_categories.items(), key=lambda item: (-item[1], item[0])):  # type: ignore[union-attr]
            lines.append(f"- {category}: {count}")
    if result.skip_reasons:
        lines.extend(["", "## Skip Reasons", ""])
        for reason, count in sorted(result.skip_reasons.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- {reason}: {count}")
    return "\n".join(lines) + "\n"


def write_summary_markdown(result: BacktestResult, path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_summary_markdown(result), encoding="utf-8")


def render_multi_date_summary_markdown(results: tuple[BacktestResult, ...]) -> str:
    lines: list[str] = [
        "# V3 Multi-Date Backtest Summary",
        "",
        f"- Runs: {len(results)}",
    ]
    if not results:
        return "\n".join(lines) + "\n"

    forward_days = results[0].config.forward_days
    summaries = [summarize_result(result) for result in results]
    total_attempted = sum(int(summary["symbols_attempted"]) for summary in summaries)
    total_processed = sum(int(summary["symbols_processed"]) for summary in summaries)
    total_skipped = sum(int(summary["symbols_skipped"]) for summary in summaries)
    total_candidates = sum(int(summary["candidates_found"]) for summary in summaries)
    aggregate_density = total_candidates / total_processed if total_processed else 0.0
    lines.extend(
        [
            f"- Stage families: {', '.join(results[0].config.stage_families)}",
            f"- Universe file: {results[0].config.universe_file}",
            f"- Symbols attempted: {total_attempted}",
            f"- Symbols processed: {total_processed}",
            f"- Symbols skipped: {total_skipped}",
            f"- Candidates found: {total_candidates}",
            f"- Candidate density: {aggregate_density:.4f}",
            "",
            "## Runs",
            "",
            "| D Date | Processed | Skipped | Candidates | Density |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for summary in summaries:
        lines.append(
            f"| {summary['d_date']} | {summary['symbols_processed']} | {summary['symbols_skipped']} | "
            f"{summary['candidates_found']} | {float(summary['candidate_density']):.4f} |"
        )

    lines.extend(["", "## Aggregate Forward Outcomes", "", "| Horizon | Evaluated | Positive | Hit Rate | Average Return | Median Return |", "|---|---:|---:|---:|---:|---:|"])
    candidate_rows = [
        row
        for result in results
        for row in result.detail_rows
        if row.get("CandidateClass") in {"SELECTED", "WATCH"}
    ]
    for days in forward_days:
        values = [_number(row.get(f"DPlus{days}ReturnPct")) for row in candidate_rows if row.get(f"DPlus{days}ReturnPct") is not None]
        numeric_values = [value for value in values if value is not None]
        positives = [value for value in numeric_values if value > 0]
        hit_rate = len(positives) / len(numeric_values) if numeric_values else 0.0
        average_return = _mean(numeric_values)
        median_return = _median(numeric_values)
        lines.append(
            f"| D+{days} | {len(numeric_values)} | {len(positives)} | {hit_rate:.2%} | "
            f"{_format_pct_value(average_return)} | {_format_pct_value(median_return)} |"
        )
    return "\n".join(lines) + "\n"


def row_value(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    return "" if value is None else str(value)


def _append_group_outcomes(
    lines: list[str],
    title: str,
    outcomes: object,
    forward_days: tuple[int, ...],
    *,
    group_order: tuple[str, ...] = (),
) -> None:
    if not isinstance(outcomes, dict) or not outcomes:
        return
    for days in forward_days:
        ordered_groups = _ordered_groups(outcomes, group_order)
        rows: list[str] = []
        for group in ordered_groups:
            metrics = outcomes.get(group)
            if not isinstance(metrics, dict):
                continue
            evaluated = int(metrics.get(f"d_plus_{days}_evaluated", 0))
            if evaluated == 0:
                continue
            candidates = int(metrics.get("candidates", 0))
            positive = int(metrics.get(f"d_plus_{days}_positive", 0))
            hit_rate = float(metrics.get(f"d_plus_{days}_hit_rate", 0.0))
            average_return = _format_pct_value(metrics.get(f"d_plus_{days}_average_return_pct"))
            median_return = _format_pct_value(metrics.get(f"d_plus_{days}_median_return_pct"))
            rows.append(
                f"| {group} | {candidates} | {evaluated} | {positive} | {hit_rate:.2%} | {average_return} | {median_return} |"
            )
        if rows:
            lines.extend(
                [
                    "",
                    f"## {title} D+{days}",
                    "",
                    "| Group | Candidates | Evaluated | Positive | Hit Rate | Average Return | Median Return |",
                    "|---|---:|---:|---:|---:|---:|---:|",
                ]
            )
            lines.extend(rows)


def _ordered_groups(outcomes: dict[object, object], group_order: tuple[str, ...]) -> list[str]:
    keys = [str(key) for key in outcomes.keys()]
    ordered = [group for group in group_order if group in keys]
    ordered.extend(sorted(group for group in keys if group not in set(ordered)))
    return ordered


def _format_pct_value(value: object) -> str:
    try:
        return "" if value is None else f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return ""


def _number(value: object) -> float | None:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 4)


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return round(ordered[midpoint], 4)
    return round((ordered[midpoint - 1] + ordered[midpoint]) / 2, 4)
