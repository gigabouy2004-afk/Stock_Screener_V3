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

from stock_screener_v3.runner import EngineRunPackResult, EngineRunResult, run_backtest, run_backtest_pack


HOST = "127.0.0.1"
PORT = 8010
DEFAULT_STAGE_FAMILIES = ("CROSSOVER", "MOMENTUM_SETUP", "DIVERGENCE")


@dataclass(frozen=True)
class WebRunResult:
    mode: str
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
    mode = values.get("mode", "single")
    stage_families = _stage_families(values)
    common = {
        "workspace_root": ROOT,
        "universe_file": values.get("universe_file", "data/samples/us_master_sample.csv"),
        "sectors": _split_csv(values.get("sector", "")),
        "exchanges": _split_csv(values.get("exchange", "")),
        "sample_size": _int_or_none(values.get("sample_size", "")),
        "random_seed": _int_or_none(values.get("random_seed", "")),
        "forward_days": tuple(int(value) for value in _split_csv(values.get("forward_days", "1,2,5"))),
        "stage_families": stage_families,
        "run_label": values.get("run_label", "v3_web_run") or "v3_web_run",
    }
    if mode == "pack":
        pack = run_backtest_pack(
            **common,
            d_dates=tuple(date.fromisoformat(value) for value in _split_csv(values.get("d_dates", ""))),
        )
        return _pack_result(pack)
    run = run_backtest(
        **common,
        d_date=date.fromisoformat(values.get("d_date", "")),
    )
    return _single_result(run)


def _single_result(run: EngineRunResult) -> WebRunResult:
    detail_rows = _read_detail_rows(run.paths.details_output)
    headline = (
        f"{run.result.config.d_date.isoformat()} | processed {run.result.symbols_processed}/"
        f"{run.result.symbols_attempted} | skipped {run.result.symbols_skipped} | "
        f"candidates {run.result.candidates_found}"
    )
    return WebRunResult(
        mode="single",
        headline=headline,
        detail_rows=detail_rows,
        artifact_rows=(
            ("Detail CSV", run.paths.details_output),
            ("Summary", run.paths.summary_output),
            ("Log", run.paths.log_file),
        ),
        summary_text=_read_text(run.paths.summary_output),
    )


def _pack_result(pack: EngineRunPackResult) -> WebRunResult:
    detail_rows: list[dict[str, str]] = []
    processed = 0
    attempted = 0
    skipped = 0
    candidates = 0
    artifacts: list[tuple[str, Path]] = [("Aggregate Summary", pack.summary_output)]
    for run in pack.runs:
        processed += run.result.symbols_processed
        attempted += run.result.symbols_attempted
        skipped += run.result.symbols_skipped
        candidates += run.result.candidates_found
        detail_rows.extend(_read_detail_rows(run.paths.details_output))
        label = run.result.config.d_date.isoformat()
        artifacts.extend(
            (
                (f"{label} Detail CSV", run.paths.details_output),
                (f"{label} Summary", run.paths.summary_output),
                (f"{label} Log", run.paths.log_file),
            )
        )
    headline = f"{len(pack.runs)} dates | processed {processed}/{attempted} | skipped {skipped} | candidates {candidates}"
    return WebRunResult(
        mode="pack",
        headline=headline,
        detail_rows=tuple(detail_rows),
        artifact_rows=tuple(artifacts),
        summary_text=_read_text(pack.summary_output),
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
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    th, td {{ border-bottom: 1px solid #e2e6ed; padding: 8px 7px; text-align: left; vertical-align: top; }}
    th {{ background: #f8fafc; font-size: 11px; color: #445064; }}
    td.num, th.num {{ text-align: right; }}
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
    <div class="status">Full engine: Crossover, Momentum Setup, Divergence</div>
  </header>
  <main>
    <aside>
      {render_form(values)}
    </aside>
    <section class="content">
      {render_result(result, error)}
    </section>
  </main>
</body>
</html>"""


def render_form(values: dict[str, str]) -> str:
    mode = values.get("mode", "single")
    return f"""<form method="post">
  <div class="panel">
    <h2>Run</h2>
    <label for="mode">Mode</label>
    <select id="mode" name="mode">
      <option value="single" {_selected(mode, "single")}>Single date</option>
      <option value="pack" {_selected(mode, "pack")}>Multi-date pack</option>
    </select>
    <label for="universe_file">Universe CSV</label>
    <input id="universe_file" name="universe_file" value="{_field(values, "universe_file", "data/samples/us_master_sample.csv")}">
    <div class="grid-2">
      <div>
        <label for="d_date">D Date</label>
        <input id="d_date" name="d_date" type="date" value="{_field(values, "d_date", "2026-02-11")}">
      </div>
      <div>
        <label for="d_dates">Pack Dates</label>
        <input id="d_dates" name="d_dates" value="{_field(values, "d_dates", "2026-02-11,2026-03-11")}">
      </div>
    </div>
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
    <label for="forward_days">Forward Days</label>
    <input id="forward_days" name="forward_days" value="{_field(values, "forward_days", "1,2,5")}">
    <label for="run_label">Run Label</label>
    <input id="run_label" name="run_label" value="{_field(values, "run_label", "v3_web_run")}">
    <button type="submit">Run V3 Engine</button>
  </div>
</form>"""


def render_stage_check(values: dict[str, str], family: str) -> str:
    raw = values.get("stage_family", "")
    selected = family in _split_csv(raw) if raw else family in DEFAULT_STAGE_FAMILIES
    checked = "checked" if selected else ""
    return f'<label class="check"><input type="checkbox" name="stage_family" value="{family}" {checked}>{family}</label>'


def render_result(result: WebRunResult | None, error: str) -> str:
    if error:
        return f'<div class="banner error">{html.escape(error)}</div>{render_empty_result()}'
    if result is None:
        return render_empty_result()
    return f"""
      <div class="banner ok">{html.escape(result.headline)}</div>
      <div class="panel">
        <h2>Artifacts</h2>
        <div class="artifacts">{render_artifacts(result.artifact_rows)}</div>
      </div>
      <div class="panel">
        <h2>Candidates</h2>
        {render_results_table(result.detail_rows)}
      </div>
      <div class="panel">
        <h2>Summary</h2>
        <div class="summary">{html.escape(result.summary_text)}</div>
      </div>
    """


def render_empty_result() -> str:
    return """<div class="panel">
      <h2>Run Result</h2>
      <p class="empty">No run submitted.</p>
    </div>"""


def render_artifacts(artifacts: tuple[tuple[str, Path], ...]) -> str:
    return "".join(
        f'<div class="artifact"><strong>{html.escape(label)}</strong><span>{html.escape(str(path))}</span></div>'
        for label, path in artifacts
    )


def render_results_table(rows: tuple[dict[str, str], ...]) -> str:
    candidates = [row for row in rows if row.get("CandidateClass") in {"SELECTED", "WATCH"}]
    visible_rows = candidates or rows
    if not visible_rows:
        return '<p class="empty">No rows emitted.</p>'
    columns = (
        "Symbol",
        "CandidateState",
        "CandidateClass",
        "StageFamily",
        "ReviewPriority",
        "TotalScore",
        "DPlus1ReturnPct",
        "OutcomeCategory",
        "FailureCategory",
    )
    body = []
    for row in visible_rows[:30]:
        body.append(
            "<tr>"
            + "".join(
                f'<td class="{"num" if column in {"TotalScore", "DPlus1ReturnPct"} else ""}">{html.escape(row.get(column, ""))}</td>'
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


def _read_detail_rows(path: Path) -> tuple[dict[str, str], ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return tuple(dict(row) for row in csv.DictReader(handle))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


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


def _field(values: dict[str, str], name: str, default: str) -> str:
    return html.escape(values.get(name, default))


def _selected(value: str, expected: str) -> str:
    return "selected" if value == expected else ""


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), V3Handler)
    print(f"Stock Screener V3 running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
