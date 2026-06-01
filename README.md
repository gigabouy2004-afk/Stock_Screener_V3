# Stock Screener Engine Rebuild 2026

This repository is the clean reset workspace for the stock screener engine.

It exists to keep the new program charter, architecture analysis, backtesting plan, implementation work, and validation evidence in one Git-tracked folder.

## Intent

Build a user-driven tactical technical-analysis scanner that can:

- Load a user-selected CSV universe containing NSE, BSE, NYSE, and NASDAQ stock codes.
- Establish market, sector, and stock context.
- Route stocks into stage families.
- Produce explainable candidates.
- Separate technical signal validity from quality, context risk, and review priority.
- Backtest the same production engine as of historical dates.

The engine is not intended to perform automated trading, position sizing, capital allocation, or order execution.

## Source Documents

- Fresh charter: [docs/charter/engine_program_charter_fresh_2026-06-01.md](docs/charter/engine_program_charter_fresh_2026-06-01.md)
- Current engine gap analysis: [docs/analysis/current_engine_gap_analysis_against_fresh_charter_2026-06-01.md](docs/analysis/current_engine_gap_analysis_against_fresh_charter_2026-06-01.md)
- V2 operational parity contract: [docs/architecture/v2_operational_parity_contract.md](docs/architecture/v2_operational_parity_contract.md)
- Current handover: [docs/handover/current_session_handover.md](docs/handover/current_session_handover.md)

Archived reference documents from the previous engine are kept under `docs/`.

## Current Decision

Do not continue tuning the old Crossover monolith.

Keep useful parts from the previous engine:

- Indicator calculations.
- Reason-code practice.
- Web app operating model.
- Historical replay concept.
- Validation artifacts and lessons.

Rebuild or refactor:

- Decision layer.
- Evidence-pack model.
- Candidate class and review-priority output.
- Backtesting subsystem.
- Metadata baseline.

## Repository Structure

```text
data/
  samples/              Sample or fixture data only. No large raw market dumps.
docs/
  analysis/             Gap analyses and current-state reviews.
  architecture/         Target architecture and module contracts.
  backtesting/          Backtesting design and validation methodology.
  charter/              Program charter and scope documents.
scripts/                Utility scripts.
src/                    Future engine implementation.
tests/                  Automated tests.
validation/
  baselines/            Accepted baseline validation summaries.
  runs/                 Dated validation outputs and notes.
```

## GitHub Remote Setup

GitHub CLI is not installed on this machine at creation time, so the remote repository was not created automatically.

After creating an empty GitHub repository manually, connect it with:

```powershell
git remote add origin https://github.com/<owner>/<repo>.git
git branch -M main
git push -u origin main
```

## Development Rule

No signal-rule change should be promoted without a backtest report that includes:

- D date or date range.
- Universe and filters.
- Symbols processed.
- Candidates found.
- Candidate density.
- D+1, D+2, and D+5 outcome.
- Score-bucket behavior.
- Failure categories.

## Current Implementation Status

Sprint 1 has started with the foundation layer:

- Python package skeleton under `src/stock_screener_v3`.
- Core dataclasses for universe records, evidence packs, stage evaluations, scores, and backtest results.
- CSV universe loader with metadata preservation for mixed NSE/BSE/NYSE/NASDAQ files.
- Sector/exchange filtering and deterministic sampling.
- Historical slicing helpers for no-lookahead tests.
- BacktestEngine v1 with pluggable price provider and stage evaluator contracts.
- Candidate-density and candidate-only forward hit-rate summaries.
- Yahoo data-provider wrapper behind a provider interface.
- Detail CSV and summary markdown report writers.
- Run I/O helpers for V2-style artifact naming under `validation/runs/`.
- V2-compatible offline CSV header contract.
- Workspace-safe input/output path resolution.
- File and console run logging with explicit logger close support for Windows.
- First production Crossover evaluator slice with deterministic daily evidence calculations.
- Reusable run orchestrator and CLI entry point.
- Initial Python web UI wrapper in `web_app_v3.py`.
- Standard-library unit tests under `tests/`.

Run tests with:

```powershell
$env:PYTHONPATH='D:\Tools\Stock_Screener_V3\src'
python -m unittest discover -s tests -v
```

Run a V3 backtest from PowerShell:

```powershell
$env:PYTHONPATH='D:\Tools\Stock_Screener_V3\src'
python -m stock_screener_v3.cli backtest --workspace-root D:\Tools\Stock_Screener_V3 --universe-file data\samples\us_master_sample.csv --d-date 2026-02-11 --forward-days 1,2,5
```

Run the initial V3 web UI:

```powershell
python D:\Tools\Stock_Screener_V3\web_app_v3.py
```

The UI opens at `http://127.0.0.1:8010`.
