# Stock Screener V3 Handover

Last updated: 2026-06-02

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `main`

Latest confirmed pushed commit: `205ee71 Add current session handover`

## Purpose Of This Document

This is the restart trace for the next session. Keep this document updated whenever the working direction, completed foundation, next step, or open risk changes.

If the computer/session restarts, start here first, then run:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -8
$env:PYTHONPATH='D:\Tools\Stock_Screener_V3\src'
python -m unittest discover -s tests -v
```

Expected status at this handover:

```text
## main...origin/main
```

Expected tests at this handover:

```text
23 tests passing
```

## Current Decision

Do not continue tuning the old V2 Crossover monolith.

V3 is a clean rebuild that should preserve the useful V2 operating model, output visibility, and validation discipline while rebuilding the engine logic with cleaner module boundaries.

The actual production signal engine/stage evaluators are not yet implemented.

## Completed Groundwork

Documentation and architecture:

- Fresh program charter.
- V2 gap analysis against the fresh charter.
- V3 initial analysis and way-forward plan.
- V3 module contracts.
- Backtesting engine requirements.
- V2 operational parity contract.
- Validation baseline acceptance pack.

Foundation code:

- Python package skeleton under `src/stock_screener_v3`.
- Core dataclasses:
  - `UniverseRecord`
  - `PriceDataBundle`
  - `EvidencePack`
  - `ScoreResult`
  - `StageEvaluation`
  - `BacktestRunConfig`
  - `BacktestResult`
- CSV universe loader with metadata preservation.
- Sector/exchange filtering.
- Deterministic sampling.
- Historical as-of slicing helpers.
- Forward-return helper.
- Backtest engine shell with pluggable price provider and stage evaluator.
- In-memory test price provider.
- Yahoo price provider wrapper.
- Detail CSV writer.
- Summary markdown writer.
- Run path and artifact helpers.
- File and console run logger with explicit close support for Windows.
- V2-compatible offline CSV column contract.
- Guardrail that log, detail CSV, and summary report must be physically separate files.

Tests:

- Universe loader tests.
- Backtesting utility tests.
- Backtest engine tests.
- Data provider tests.
- Report/output contract tests.
- Run I/O and log artifact tests.

## Artifact Purpose Definitions

These definitions are settled and should not drift:

- Log file: execution summary report for the run.
- Output CSV: forensic calculation record for each symbol/code.
- Summary markdown: human-readable run summary.

The output CSV must preserve the V2-compatible header block first, then append V3-specific fields.

The CSV writer must emit headers even when zero candidates are found.

## Important Files

Core source:

- `src/stock_screener_v3/models.py`
- `src/stock_screener_v3/universe.py`
- `src/stock_screener_v3/backtesting.py`
- `src/stock_screener_v3/backtest_engine.py`
- `src/stock_screener_v3/data_provider.py`
- `src/stock_screener_v3/reports.py`
- `src/stock_screener_v3/run_io.py`
- `src/stock_screener_v3/output_contracts.py`

Key docs:

- `docs/charter/engine_program_charter_fresh_2026-06-01.md`
- `docs/analysis/current_engine_gap_analysis_against_fresh_charter_2026-06-01.md`
- `docs/analysis/v3_initial_engine_analysis_and_way_forward_2026-06-01.md`
- `docs/architecture/v3_module_contracts.md`
- `docs/architecture/rebuild_way_forward_plan.md`
- `docs/architecture/v2_operational_parity_contract.md`
- `docs/backtesting/backtesting_engine_requirements.md`
- `validation/baselines/v3_baseline_acceptance_pack.md`

Tests:

- `tests/test_universe.py`
- `tests/test_backtesting.py`
- `tests/test_backtest_engine.py`
- `tests/test_data_provider.py`
- `tests/test_reports.py`
- `tests/test_run_io.py`

## Recent Commit Trace

```text
205ee71 Add current session handover
05c5953 Clarify log and output artifact purposes
6e3f40b Enforce separate run forensic artifacts
f808289 Preserve V2 output parity contract
4f505ef Add V3 run artifact IO validation
183b3e1 Add V3 data provider and backtest reports
5e244a6 Add V3 backtesting engine foundation
99b431c Add V3 foundation models and universe loader
71c759a Add V3 analysis and execution plan
```

## What Is Not Yet Built

The actual V3 production engine logic is not implemented yet:

- No production `EvidencePack` builder.
- No production Crossover evaluator.
- No production Momentum Trading evaluator.
- No production Divergence evaluator.
- No scoring calibration beyond data model contracts.
- No V3 web UI yet.
- No CLI adapter that runs the whole V3 engine end to end.
- No live execution workflow beyond provider/report/run I/O foundations.

## Recommended Next Session Start

Start with the production engine design, not the UI.

Recommended next implementation order:

1. Create an evidence-builder module that converts `PriceDataBundle` into `EvidencePack`.
2. Port only stable, useful V2 indicator calculations into clean helper functions.
3. Implement the first production `StageEvaluator`, probably Crossover, with separated outputs:
   - route validity
   - timing
   - structure
   - participation
   - context risk
   - final `CandidateClass`
   - `ReviewPriority`
   - reason codes
4. Run the evaluator through the existing backtest engine on fixed historical D dates.
5. Only after the engine produces explainable candidates, build the V3 CLI/web adapter.

## Carry-Forward Rules

- Do not hide technical signal validity because of quality/context concerns. Use `CandidateClass`, `ReviewPriority`, and risk tags instead.
- Do not tune a rule from one stock/event.
- Do not promote signal-rule changes without a backtest report.
- Preserve sector/exchange metadata from the input universe in output rows.
- Preserve V2-compatible offline CSV headers.
- Keep log, output CSV, and summary report separate.
- Keep the handover document updated after every meaningful change.
