from __future__ import annotations

from datetime import date
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from stock_screener_v3.runner import run_backtest


HOST = "127.0.0.1"
PORT = 8010


class V3Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self._send_html(render_page())

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        values = {key: value[-1] for key, value in parse_qs(self.rfile.read(length).decode("utf-8")).items()}
        try:
            d_date = date.fromisoformat(values.get("d_date", ""))
            run = run_backtest(
                workspace_root=ROOT,
                universe_file=values.get("universe_file", "data/samples/us_master_sample.csv"),
                d_date=d_date,
                sectors=_split_csv(values.get("sector", "")),
                exchanges=_split_csv(values.get("exchange", "")),
                sample_size=_int_or_none(values.get("sample_size", "")),
                random_seed=_int_or_none(values.get("random_seed", "")),
                forward_days=tuple(int(value) for value in _split_csv(values.get("forward_days", "1,2,5"))),
                run_label=values.get("run_label", "v3_backtest") or "v3_backtest",
            )
            message = (
                f"Processed {run.result.symbols_processed} of {run.result.symbols_attempted}; "
                f"candidates {run.result.candidates_found}. "
                f"Output CSV: {run.paths.details_output}. "
                f"Summary: {run.paths.summary_output}. "
                f"Log: {run.paths.log_file}."
            )
            self._send_html(render_page(message=message))
        except Exception as exc:
            self._send_html(render_page(error=str(exc)))

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def render_page(message: str = "", error: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Stock Screener V3</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Arial, sans-serif;
      background: #f6f7f9;
      color: #1d2430;
    }}
    body {{ margin: 0; }}
    header {{
      background: #ffffff;
      border-bottom: 1px solid #d8dde6;
      padding: 18px 24px;
    }}
    h1 {{ font-size: 22px; margin: 0; }}
    main {{
      display: grid;
      grid-template-columns: 340px minmax(0, 1fr);
      gap: 18px;
      padding: 18px;
    }}
    section {{
      background: #ffffff;
      border: 1px solid #d8dde6;
      border-radius: 6px;
      padding: 16px;
    }}
    label {{ display: block; font-size: 13px; font-weight: 700; margin: 12px 0 5px; }}
    input {{
      box-sizing: border-box;
      width: 100%;
      border: 1px solid #b8c0cc;
      border-radius: 4px;
      padding: 9px 10px;
      font-size: 14px;
    }}
    button {{
      margin-top: 16px;
      width: 100%;
      border: 0;
      border-radius: 4px;
      padding: 10px 12px;
      background: #2454a6;
      color: #ffffff;
      font-weight: 700;
      cursor: pointer;
    }}
    .message, .error {{
      border-radius: 4px;
      padding: 12px;
      line-height: 1.45;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .message {{ background: #eef8f1; border: 1px solid #b6dfc2; }}
    .error {{ background: #fff0f0; border: 1px solid #efb5b5; }}
    .empty {{ color: #687386; }}
    dl {{ display: grid; grid-template-columns: 160px minmax(0, 1fr); gap: 8px 12px; }}
    dt {{ font-weight: 700; }}
    dd {{ margin: 0; overflow-wrap: anywhere; }}
    @media (max-width: 860px) {{
      main {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header><h1>Stock Screener V3</h1></header>
  <main>
    <section>
      <form method="post">
        <label for="universe_file">Universe CSV</label>
        <input id="universe_file" name="universe_file" value="data/samples/us_master_sample.csv">
        <label for="d_date">D Date</label>
        <input id="d_date" name="d_date" type="date" value="2026-02-11">
        <label for="sector">Sector Filter</label>
        <input id="sector" name="sector" placeholder="Technology,Energy,Industrials">
        <label for="exchange">Exchange Filter</label>
        <input id="exchange" name="exchange" placeholder="NYSE,NASDAQ">
        <label for="sample_size">Sample Size</label>
        <input id="sample_size" name="sample_size" type="number" min="1" placeholder="Optional">
        <label for="random_seed">Random Seed</label>
        <input id="random_seed" name="random_seed" type="number" placeholder="Optional">
        <label for="forward_days">Forward Days</label>
        <input id="forward_days" name="forward_days" value="1,2,5">
        <label for="run_label">Run Label</label>
        <input id="run_label" name="run_label" value="v3_backtest">
        <button type="submit">Run Engine</button>
      </form>
    </section>
    <section>
      <h2>Run Result</h2>
      {render_result_block(message, error)}
      <h2>Artifact Purpose</h2>
      <dl>
        <dt>Log</dt><dd>Execution summary report for the run.</dd>
        <dt>Output CSV</dt><dd>Forensic calculation record for each symbol/code.</dd>
        <dt>Summary</dt><dd>Human-readable run summary.</dd>
      </dl>
    </section>
  </main>
</body>
</html>"""


def render_result_block(message: str, error: str) -> str:
    if error:
        return f'<div class="error">{html.escape(error)}</div>'
    if message:
        return f'<div class="message">{html.escape(message)}</div>'
    return '<p class="empty">No run submitted yet.</p>'


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())


def _int_or_none(value: str) -> int | None:
    return int(value) if value.strip() else None


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), V3Handler)
    print(f"Stock Screener V3 running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
