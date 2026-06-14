# Stock Screener Engine Rebuild 2026

This repository is the clean reset workspace for the stock screener engine.

It exists to keep the new program charter, architecture analysis, backtesting plan, implementation work, and validation evidence in one Git-tracked folder.

## Intent

The active charter branch is now `V3_charter`.

This branch is the root-start branch from `main` for the June 12/13 charter documentation direction.

The new canonical entry points for active work are:

- [docs/charter/engine_program_charter_fresh_2026-06-01.md](docs/charter/engine_program_charter_fresh_2026-06-01.md)
- [docs/charter/v3_original_intent_and_handover.md](docs/charter/v3_original_intent_and_handover.md)
- [docs/architecture/main_engine_way_forward_plan.md](docs/architecture/main_engine_way_forward_plan.md)
- [docs/handover/main_engine_startup_handover.md](docs/handover/main_engine_startup_handover.md)

Older V3 documents remain in the repo as historical references.

At the core, V3 is a CSV-based, user-directed stock analysis engine with exactly three user-facing analysis paths:

- `CROSSOVER`
- `DIVERGENCE`
- `MOMENTUM_SETUP` / `BULL_EXTENSION`

The engine must preserve the V2 path-first architecture, including baseline analysis, path routing, path-specific evidence, date processing, and D+X self-backtesting.

Broader context work below is historical/background unless explicitly requested by the user for a specific step.

Previous broad rebuild language:

- Load a user-selected CSV universe containing NSE, BSE, NYSE, and NASDAQ stock codes.
- Establish market, sector, and stock context.
- Route stocks into stage families.
- Produce explainable candidates.
- Separate technical signal validity from quality, context risk, and review priority.
- Backtest the same production engine as of historical dates.

The engine is not intended to perform automated trading, position sizing, capital allocation, or order execution.

## Source Documents

- Canonical V3 original intent and handover: [docs/charter/v3_original_intent_and_handover.md](docs/charter/v3_original_intent_and_handover.md)
- Fresh charter: [docs/charter/engine_program_charter_fresh_2026-06-01.md](docs/charter/engine_program_charter_fresh_2026-06-01.md)
- Current engine gap analysis: [docs/analysis/current_engine_gap_analysis_against_fresh_charter_2026-06-01.md](docs/analysis/current_engine_gap_analysis_against_fresh_charter_2026-06-01.md)
- V2 operational parity contract: [docs/architecture/v2_operational_parity_contract.md](docs/architecture/v2_operational_parity_contract.md)
- V3 evidence-stage matrix: [docs/architecture/v3_evidence_stage_matrix.md](docs/architecture/v3_evidence_stage_matrix.md)
- V3 baseline decision tree: [docs/architecture/v3_baseline_decision_tree.md](docs/architecture/v3_baseline_decision_tree.md)
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

Sprint 1 has produced the foundation layer and a V1-complete Crossover family:

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
- Crossover stage family V1 complete for the current engine scope:
  - deterministic daily MACD/RSI/ADX/EMA/volume/structure evidence;
  - direction-aware bull transition entry and bear transition exit/preservation routes;
  - below-zero MACD pair requirement for bullish Crossover transition;
  - explicit rejection of above-zero bull continuation as Crossover;
  - generated cross-sector and symbol-level calibration reports from existing detail CSVs.
- First Momentum Setup evaluator slice for bull pullback re-entry and bull continuation.
- Stage-family dispatcher and CLI stage-family selection for Crossover, Momentum Setup, Divergence, or any restricted subset.
- Formal ranking diagnostics for choosing the reported stage-family result after holistic traversal.
- Baseline router with market/sector/stock regime diagnostics and positive elimination.
- Configurable market/sector/theme benchmark mapping for regime determination.
- Single-date backtest CLI that runs the same V3 evidence, traversal, ranking, and report path used by the production engine layer.
- Reusable run orchestrator and CLI entry point.
- Python scanner console in `web_app_v3.py` for user-selected V3 scans with V2-style stage classifications and visible diagnostics.
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

The default stage-family set is `CROSSOVER,MOMENTUM_SETUP,DIVERGENCE`. Use `--stage-family` only when intentionally restricting the engine path.

Run a multi-date V3 backtest pack:

```powershell
$env:PYTHONPATH='D:\Tools\Stock_Screener_V3\src'
python -m stock_screener_v3.cli backtest-pack --workspace-root D:\Tools\Stock_Screener_V3 --universe-file data\samples\us_master_sample.csv --d-dates 2026-02-11,2026-03-11 --forward-days 1,2,5
```

Generate Crossover calibration reports from existing detail CSVs:

```powershell
$env:PYTHONPATH='D:\Tools\Stock_Screener_V3\src'
python -m stock_screener_v3.cli cross-sector-report --details <comma-separated-detail-csvs> --output validation\runs\cross_sector_report.md --horizon-days 20 --candidate-state PRE_BEAR_CROSSOVER
python -m stock_screener_v3.cli symbol-failure-report --details <comma-separated-detail-csvs> --output validation\runs\symbol_failure_report.md --horizon-days 20
python -m stock_screener_v3.cli stage-family-report --details <comma-separated-detail-csvs> --output validation\runs\stage_family_report.md --stage-family DIVERGENCE --horizon-days 20
python -m stock_screener_v3.cli integrated-report --details <comma-separated-detail-csvs> --output validation\runs\integrated_report.md --horizon-days 20
```

Run the V3 web console:

```powershell
python D:\Tools\Stock_Screener_V3\web_app_v3.py
```

The UI opens at `http://127.0.0.1:8010`.

## Current Next Plan

The Crossover, Divergence, and Momentum Setup stage families are V1 complete and tested for the current engine scope.

Integrated holistic validation now has a repeatable report command and baseline artifact:

- `python -m stock_screener_v3.cli integrated-report ...`
- `validation/runs/v3_integrated_holistic_calibration_20260611.md`

The next focus is review-priority and collision-slice calibration:

- inspect weak ranking buckets `MOMENTUM_SETUP` and `DIVERGENCE+MOMENTUM_SETUP`;
- review `NEEDS_MANUAL_REVIEW` and `BELOW_EMA200` calibration across sectors and D dates;
- decide whether a sector/date/context urgency layer is warranted before threshold changes;
- keep enriched universe metadata/filtering as the parallel data-quality track.
