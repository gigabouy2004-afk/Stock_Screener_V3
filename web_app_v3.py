from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import csv
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from stock_screener_v3.runner import EngineRunResult, run_backtest


HOST = "127.0.0.1"
PORT = 8010
DEFAULT_STAGE_FAMILIES = ("CROSSOVER", "MOMENTUM_SETUP", "DIVERGENCE")
STAGE_CLASSIFICATIONS = (
    ("PRE_BULL_CROSSOVER", "Pre-Bull Crossover", "Bull transition / new capital review.", "bull"),
    ("PRE_BEAR_CROSSOVER", "Pre-Bear Crossover", "Bear transition / exit or preservation review.", "bear"),
    ("BULLISH_DIVERGENCE", "Bullish Divergence", "Price/momentum disagreement for bullish reversal watch.", "bull"),
    ("BEARISH_DIVERGENCE", "Bearish Divergence", "Price/momentum disagreement for bearish exhaustion watch.", "bear"),
    ("HIDDEN_BULLISH_DIVERGENCE", "Hidden Bullish Divergence", "Bull trend continuation / pullback absorption.", "bull"),
    ("HIDDEN_BEARISH_DIVERGENCE", "Hidden Bearish Divergence", "Bear trend continuation / failed recovery.", "bear"),
    ("BULL_PULLBACK_REENTRY", "Bull Pullback Re-entry", "Momentum Setup re-entry candidate.", "bull"),
    ("BULL_CONTINUATION_MOMENTUM", "Bull Continuation Momentum", "Momentum Setup continuation candidate.", "bull"),
    ("STATUS_QUO", "Status Quo", "No selected stage route promoted.", "neutral"),
)
STAGE_LABELS = {state: label for state, label, _description, _tone in STAGE_CLASSIFICATIONS}
REVIEW_INTENTS = {
    "PRE_BULL_CROSSOVER": ("Bullish entry / re-entry", "entry"),
    "PRE_BEAR_CROSSOVER": ("Exit / preservation", "exit"),
    "BULLISH_DIVERGENCE": ("Bullish entry / re-entry", "entry"),
    "HIDDEN_BULLISH_DIVERGENCE": ("Bullish entry / re-entry", "entry"),
    "BULL_PULLBACK_REENTRY": ("Bullish entry / re-entry", "entry"),
    "BULL_CONTINUATION_MOMENTUM": ("Bullish entry / re-entry", "entry"),
    "BEARISH_DIVERGENCE": ("Bearish risk review", "bear"),
    "HIDDEN_BEARISH_DIVERGENCE": ("Bearish risk review", "bear"),
    "STATUS_QUO": ("Status / no route", "neutral"),
}
REVIEW_SPLIT_ORDER = (
    ("entry", "Bullish entry / re-entry"),
    ("exit", "Exit / preservation"),
    ("bear", "Bearish risk review"),
    ("neutral", "Status / no route"),
)


@dataclass(frozen=True)
class WebRunResult:
    headline: str
    detail_rows: tuple[dict[str, str], ...]
    artifact_rows: tuple[tuple[str, Path], ...]
    summary_text: str


class V3Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self._send_html(render_page())

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        parsed_values = parse_qs(self.rfile.read(length).decode("utf-8"))
        values = {key: value[-1] for key, value in parsed_values.items()}
        if "stage_family" in parsed_values:
            values["stage_family"] = ",".join(parsed_values["stage_family"])
        try:
            result = execute_run(values)
            self._send_html(render_page(result=result, form_values=values))
        except Exception as exc:
            self._send_html(render_page(error=str(exc), form_values=values))

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def execute_run(values: dict[str, str]) -> WebRunResult:
    stage_families = _stage_families(values)
    run = run_backtest(
        workspace_root=ROOT,
        universe_file=values.get("universe_file", "data/samples/us_master_sample.csv"),
        d_date=date.fromisoformat(values.get("d_date", "")),
        sectors=_split_csv(values.get("sector", "")),
        exchanges=_split_csv(values.get("exchange", "")),
        sample_size=_int_or_none(values.get("sample_size", "")),
        random_seed=_int_or_none(values.get("random_seed", "")),
        forward_days=(1, 2, 5),
        stage_families=stage_families,
        run_label=values.get("run_label", "v3_scan") or "v3_scan",
    )
    return _single_result(run)


def _single_result(run: EngineRunResult) -> WebRunResult:
    detail_rows = _read_detail_rows(run.paths.details_output)
    headline = (
        f"Scan date {run.result.config.d_date.isoformat()} | processed {run.result.symbols_processed}/"
        f"{run.result.symbols_attempted} | skipped {run.result.symbols_skipped} | "
        f"candidates {run.result.candidates_found}"
    )
    return WebRunResult(
        headline=headline,
        detail_rows=detail_rows,
        artifact_rows=(
            ("Output CSV", run.paths.details_output),
            ("Summary Report", run.paths.summary_output),
            ("Run Log", run.paths.log_file),
        ),
        summary_text=_scan_summary_text(run.paths.summary_output),
    )


def render_page(
    *,
    result: WebRunResult | None = None,
    error: str = "",
    form_values: dict[str, str] | None = None,
) -> str:
    values = form_values or {}
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Stock Screener V3</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Arial, Helvetica, sans-serif;
      background: #f4f6f8;
      color: #18202c;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; }}
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      padding: 14px 20px;
      background: #ffffff;
      border-bottom: 1px solid #d7dde6;
    }}
    h1 {{ font-size: 20px; margin: 0; font-weight: 700; }}
    h2 {{ font-size: 15px; margin: 0 0 12px; }}
    .status {{ font-size: 12px; color: #556171; }}
    main {{
      display: grid;
      grid-template-columns: minmax(330px, 380px) minmax(0, 1fr);
      min-height: calc(100vh - 52px);
    }}
    aside {{
      padding: 16px;
      border-right: 1px solid #d7dde6;
      background: #ffffff;
    }}
    .content {{ padding: 16px; min-width: 0; }}
    .panel {{
      background: #ffffff;
      border: 1px solid #d7dde6;
      border-radius: 6px;
      padding: 14px;
      margin-bottom: 14px;
    }}
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    label {{ display: block; font-size: 12px; font-weight: 700; margin: 10px 0 5px; color: #273142; }}
    input, select {{
      width: 100%;
      border: 1px solid #aeb8c5;
      border-radius: 4px;
      padding: 8px 9px;
      font-size: 13px;
      background: #ffffff;
      color: #18202c;
    }}
    .checks {{ display: grid; grid-template-columns: 1fr; gap: 6px; margin-top: 6px; }}
    .check {{
      display: flex;
      align-items: center;
      gap: 8px;
      border: 1px solid #d7dde6;
      border-radius: 4px;
      padding: 7px 8px;
      font-size: 12px;
      font-weight: 700;
    }}
    .check input {{ width: auto; }}
    button {{
      width: 100%;
      margin-top: 14px;
      border: 1px solid #17417f;
      border-radius: 4px;
      padding: 10px 12px;
      background: #1f5da8;
      color: #ffffff;
      font-weight: 700;
      cursor: pointer;
    }}
    .banner {{
      border-radius: 4px;
      padding: 10px 12px;
      margin-bottom: 14px;
      font-size: 13px;
      line-height: 1.4;
      overflow-wrap: anywhere;
    }}
    .ok {{ background: #eef7f0; border: 1px solid #b8ddc1; color: #163f24; }}
    .error {{ background: #fff0f0; border: 1px solid #e6b2b2; color: #7d2020; }}
    .artifacts {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 8px;
    }}
    .artifact {{
      border: 1px solid #d7dde6;
      border-radius: 4px;
      padding: 9px;
      min-width: 0;
    }}
    .artifact strong {{ display: block; font-size: 12px; margin-bottom: 4px; }}
    .artifact span {{ display: block; font-size: 12px; color: #556171; overflow-wrap: anywhere; }}
    .stage-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 8px;
    }}
    .stage-card {{
      border: 1px solid #d7dde6;
      border-left: 4px solid #7a8797;
      border-radius: 4px;
      padding: 9px;
      min-height: 76px;
    }}
    .stage-card.bull {{ border-left-color: #25824f; }}
    .stage-card.bear {{ border-left-color: #b54545; }}
    .stage-card.neutral {{ border-left-color: #6b7789; }}
    .stage-card strong {{ display: block; font-size: 12px; margin-bottom: 4px; }}
    .stage-card span {{ display: block; color: #556171; font-size: 11px; line-height: 1.35; }}
    .stage-count {{ float: right; font-size: 18px; color: #18202c; }}
    .intent-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 8px;
    }}
    .intent-card {{
      border: 1px solid #d7dde6;
      border-left: 4px solid #7a8797;
      border-radius: 4px;
      padding: 9px;
      min-height: 58px;
      background: #ffffff;
    }}
    .intent-card.entry {{ border-left-color: #25824f; }}
    .intent-card.exit {{ border-left-color: #b54545; background: #fff8f4; }}
    .intent-card.bear {{ border-left-color: #8b4a2f; background: #fffaf4; }}
    .intent-card.neutral {{ border-left-color: #6b7789; }}
    .intent-card strong {{ display: block; font-size: 12px; margin-bottom: 4px; }}
    .intent-count {{ float: right; font-size: 18px; color: #18202c; }}
    .chip {{
      display: inline-block;
      border: 1px solid #ccd4df;
      border-radius: 999px;
      padding: 2px 7px;
      font-size: 11px;
      background: #f8fafc;
      color: #334054;
    }}
    .chip.entry {{ border-color: #a8d8b8; background: #effaf2; color: #174b2c; }}
    .chip.exit {{ border-color: #e0aaa0; background: #fff0ec; color: #7d2020; }}
    .chip.bear {{ border-color: #dfbea6; background: #fff5ea; color: #6c321b; }}
    .chip.neutral {{ border-color: #ccd4df; background: #f8fafc; color: #334054; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    th, td {{ border-bottom: 1px solid #e2e6ed; padding: 8px 7px; text-align: left; vertical-align: top; }}
    th {{ background: #f8fafc; font-size: 11px; color: #445064; }}
    td.num, th.num {{ text-align: right; }}
    tr.row-exit td {{ background: #fffaf7; }}
    tr.row-bear td {{ background: #fffdf8; }}
    .summary {{
      max-height: 430px;
      overflow: auto;
      white-space: pre-wrap;
      font-family: Consolas, monospace;
      font-size: 12px;
      line-height: 1.45;
      background: #f8fafc;
      border: 1px solid #d7dde6;
      border-radius: 4px;
      padding: 12px;
    }}
    .empty {{ color: #657185; font-size: 13px; }}
    @media (max-width: 900px) {{
      main {{ grid-template-columns: 1fr; }}
      aside {{ border-right: 0; border-bottom: 1px solid #d7dde6; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Stock Screener V3</h1>
    <div class="status">Scanner engine: Crossover, Momentum Setup, Divergence</div>
  </header>
  <main>
    <aside>
      {render_form(values)}
    </aside>
    <section class="content">
      {render_result(result, error, values)}
    </section>
  </main>
</body>
</html>"""


def render_form(values: dict[str, str]) -> str:
    return f"""<form method="post">
  <div class="panel">
    <h2>Scan</h2>
    <label for="universe_file">Universe CSV</label>
    <input id="universe_file" name="universe_file" value="{_field(values, "universe_file", "data/samples/us_master_sample.csv")}">
    <label for="d_date">Scan Date</label>
    <input id="d_date" name="d_date" type="date" value="{_field(values, "d_date", "2026-02-11")}">
    <label>Stage Families</label>
    <div class="checks">
      {render_stage_check(values, "CROSSOVER")}
      {render_stage_check(values, "MOMENTUM_SETUP")}
      {render_stage_check(values, "DIVERGENCE")}
    </div>
  </div>
  <div class="panel">
    <h2>Filters</h2>
    <label for="sector">Sector</label>
    <input id="sector" name="sector" value="{_field(values, "sector", "")}" placeholder="Technology,Energy">
    <label for="exchange">Exchange</label>
    <input id="exchange" name="exchange" value="{_field(values, "exchange", "")}" placeholder="NYSE,NASDAQ">
    <div class="grid-2">
      <div>
        <label for="sample_size">Sample Size</label>
        <input id="sample_size" name="sample_size" type="number" min="1" value="{_field(values, "sample_size", "")}">
      </div>
      <div>
        <label for="random_seed">Random Seed</label>
        <input id="random_seed" name="random_seed" type="number" value="{_field(values, "random_seed", "")}">
      </div>
    </div>
    <label for="run_label">Run Label</label>
    <input id="run_label" name="run_label" value="{_field(values, "run_label", "v3_scan")}">
    <label for="candidate_state_filter">Candidate State Filter</label>
    <input id="candidate_state_filter" name="candidate_state_filter" value="{_field(values, "candidate_state_filter", "")}" placeholder="PRE_BULL_CROSSOVER,BULLISH_DIVERGENCE">
    <div class="grid-2">
      <div>
        <label for="candidate_class_filter">Class Filter</label>
        <input id="candidate_class_filter" name="candidate_class_filter" value="{_field(values, "candidate_class_filter", "SELECTED,WATCH")}" placeholder="SELECTED,WATCH,STATUS_QUO">
      </div>
      <div>
        <label for="min_score">Min Score</label>
        <input id="min_score" name="min_score" type="number" step="0.01" value="{_field(values, "min_score", "")}">
      </div>
    </div>
    <label class="check"><input type="checkbox" name="show_status_quo" value="1" {_checked(values.get("show_status_quo", "") == "1")}>Show STATUS_QUO rows</label>
    <button type="submit">Run Scan</button>
  </div>
</form>"""


def render_stage_check(values: dict[str, str], family: str) -> str:
    raw = values.get("stage_family", "")
    selected = family in _split_csv(raw) if raw else family in DEFAULT_STAGE_FAMILIES
    checked = "checked" if selected else ""
    return f'<label class="check"><input type="checkbox" name="stage_family" value="{family}" {checked}>{family}</label>'


def render_result(result: WebRunResult | None, error: str, values: dict[str, str]) -> str:
    if error:
        return f'<div class="banner error">{html.escape(error)}</div>{render_empty_result()}'
    if result is None:
        return render_empty_result()
    filtered_rows = _filter_rows(result.detail_rows, values)
    return f"""
      <div class="banner ok">{html.escape(result.headline)}</div>
      <div class="panel">
        <h2>Stage Classifications</h2>
        {render_stage_classifications(result.detail_rows)}
      </div>
      <div class="panel">
        <h2>Review Split</h2>
        {render_review_split(filtered_rows)}
      </div>
      <div class="panel">
        <h2>Artifacts</h2>
        <div class="artifacts">{render_artifacts(result.artifact_rows)}</div>
      </div>
      <div class="panel">
        <h2>Candidates</h2>
        {render_results_table(filtered_rows)}
      </div>
      <div class="panel">
        <h2>Summary</h2>
        <div class="summary">{html.escape(result.summary_text)}</div>
      </div>
    """


def render_empty_result() -> str:
    return f"""<div class="panel">
      <h2>Stage Classifications</h2>
      {render_stage_classifications(())}
    </div>
    <div class="panel">
      <h2>Scan Result</h2>
      <p class="empty">No run submitted.</p>
    </div>"""


def render_artifacts(artifacts: tuple[tuple[str, Path], ...]) -> str:
    return "".join(
        f'<div class="artifact"><strong>{html.escape(label)}</strong><span>{html.escape(str(path))}</span></div>'
        for label, path in artifacts
    )


def render_stage_classifications(rows: tuple[dict[str, str], ...]) -> str:
    counts = _stage_counts(rows)
    cards = []
    for state, label, description, tone in STAGE_CLASSIFICATIONS:
        cards.append(
            f'<div class="stage-card {tone}"><span class="stage-count">{counts.get(state, 0)}</span>'
            f"<strong>{html.escape(label)}</strong><span>{html.escape(state)}</span><span>{html.escape(description)}</span></div>"
        )
    return '<div class="stage-grid">' + "".join(cards) + "</div>"


def render_review_split(rows: tuple[dict[str, str], ...]) -> str:
    counts = {tone: 0 for tone, _label in REVIEW_SPLIT_ORDER}
    for row in rows:
        _label, tone = _review_intent(row)
        counts[tone] = counts.get(tone, 0) + 1
    cards = [
        f'<div class="intent-card {tone}"><span class="intent-count">{counts.get(tone, 0)}</span>'
        f"<strong>{html.escape(label)}</strong></div>"
        for tone, label in REVIEW_SPLIT_ORDER
    ]
    return '<div class="intent-grid">' + "".join(cards) + "</div>"


def render_results_table(rows: tuple[dict[str, str], ...]) -> str:
    if not rows:
        return '<p class="empty">No rows emitted.</p>'
    columns = (
        "Symbol",
        "CompanyName",
        "Exchange",
        "Sector",
        "Industry",
        "LatestPrice",
        "CandidateState",
        "CandidateStateRaw",
        "CandidateClass",
        "StageClassification",
        "ReviewIntent",
        "StageFamily",
        "ReviewPriority",
        "Confidence",
        "WeightedScore",
        "TotalScore",
        "RSI_1D",
        "ADX_1D",
        "Bollinger_PctB",
        "MACD_1D_CrossoverState",
        "MACD_1D_Histogram",
        "RankingWinnerFamily",
        "DPlus1ReturnPct",
        "OutcomeCategory",
        "FailureCategory",
        "ReasonCodes",
    )
    body = []
    for row in rows[:100]:
        _label, tone = _review_intent(row)
        body.append(
            f'<tr class="row-{tone}">'
            + "".join(
                _table_cell(row, column)
                for column in columns
            )
            + "</tr>"
        )
    return (
        "<table><thead><tr>"
        + "".join(f'<th class="{"num" if column in {"TotalScore", "DPlus1ReturnPct"} else ""}">{column}</th>' for column in columns)
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
    )


def _table_cell(row: dict[str, str], column: str) -> str:
    numeric_columns = {"LatestPrice", "WeightedScore", "TotalScore", "RSI_1D", "ADX_1D", "Bollinger_PctB", "MACD_1D_Histogram", "DPlus1ReturnPct"}
    value = _display_value(row, column)
    class_name = "num" if column in numeric_columns else ""
    if column == "CandidateState":
        _label, tone = _review_intent(row)
        return f'<td><span class="chip {tone}">{html.escape(value)}</span></td>'
    if column == "ReviewIntent":
        _label, tone = _review_intent(row)
        return f'<td><span class="chip {tone}">{html.escape(value)}</span></td>'
    return f'<td class="{class_name}">{html.escape(value)}</td>'


def _read_detail_rows(path: Path) -> tuple[dict[str, str], ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return tuple(dict(row) for row in csv.DictReader(handle))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _scan_summary_text(path: Path) -> str:
    return _read_text(path).replace("V3 Backtest Summary", "V3 Scan Summary").replace("- D date:", "- Scan date:")


def _filter_rows(rows: tuple[dict[str, str], ...], values: dict[str, str]) -> tuple[dict[str, str], ...]:
    state_filter = set(_split_csv(values.get("candidate_state_filter", "")))
    class_filter = set(_split_csv(values.get("candidate_class_filter", "SELECTED,WATCH")))
    min_score = _float_or_none(values.get("min_score", ""))
    show_status_quo = values.get("show_status_quo", "") == "1"
    filtered = []
    for row in rows:
        if state_filter and row.get("CandidateState") not in state_filter:
            continue
        candidate_class = row.get("CandidateClass", "")
        if class_filter and candidate_class not in class_filter:
            if not (show_status_quo and candidate_class == "STATUS_QUO"):
                continue
        if not show_status_quo and candidate_class == "STATUS_QUO":
            continue
        if min_score is not None and (_float_or_none(row.get("TotalScore", "")) or 0.0) < min_score:
            continue
        filtered.append(row)
    return tuple(filtered)


def _stage_counts(rows: tuple[dict[str, str], ...]) -> dict[str, int]:
    counts: dict[str, int] = {state: 0 for state, _label, _description, _tone in STAGE_CLASSIFICATIONS}
    for row in rows:
        state = row.get("CandidateState", "STATUS_QUO") or "STATUS_QUO"
        counts[state] = counts.get(state, 0) + 1
    return counts


def _display_value(row: dict[str, str], column: str) -> str:
    if column == "StageClassification":
        return STAGE_LABELS.get(row.get("CandidateState", ""), row.get("CandidateState", ""))
    if column == "ReviewIntent":
        label, _tone = _review_intent(row)
        return label
    if column == "ReasonCodes":
        return row.get("ReasonCodes") or row.get("CrossoverReasonCodes") or row.get("MomentumSetupReasonCodes") or row.get("DivergenceReasonCodes") or ""
    return row.get(column, "")


def _review_intent(row: dict[str, str]) -> tuple[str, str]:
    state = row.get("CandidateState") or row.get("CandidateStateRaw") or "STATUS_QUO"
    return REVIEW_INTENTS.get(state, ("Manual review", "neutral"))


def _stage_families(values: dict[str, str]) -> tuple[str, ...]:
    raw = values.get("stage_family", "")
    if raw:
        selected = tuple(part.strip() for part in raw.split(",") if part.strip())
    elif not values:
        selected = DEFAULT_STAGE_FAMILIES
    else:
        selected = ()
    if not selected:
        raise ValueError("At least one stage family must be selected.")
    return selected


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())


def _int_or_none(value: str) -> int | None:
    return int(value) if value.strip() else None


def _float_or_none(value: str) -> float | None:
    try:
        return float(value) if value.strip() else None
    except ValueError:
        return None


def _field(values: dict[str, str], name: str, default: str) -> str:
    return html.escape(values.get(name, default))


def _selected(value: str, expected: str) -> str:
    return "selected" if value == expected else ""


def _checked(value: bool) -> str:
    return "checked" if value else ""


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), V3Handler)
    print(f"Stock Screener V3 running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
