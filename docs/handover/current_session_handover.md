# Stock Screener V3 Handover

Last updated: 2026-06-02

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `main`

Latest confirmed pushed code baseline before signoff documentation: `6df0f7e Mark regime engine v1 complete`

## Purpose Of This Document

This is the restart trace for the next session. Keep this document updated whenever the working direction, completed foundation, next step, or open risk changes.

Canonical signoff/restart document for the current transition:

- `docs/handover/transition_signoff_2026-06-02.md`

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
43 tests passing
```

## Current Decision

Do not continue tuning the old V2 Crossover monolith.

V3 is a clean rebuild that should preserve the useful V2 operating model, output visibility, and validation discipline while rebuilding the engine logic with cleaner module boundaries.

The same engine must support both new capital entry and existing capital exit/preservation:

- `PRE_BULL_CROSSOVER`: bull transition / new capital entry review.
- `PRE_BEAR_CROSSOVER`: bear transition / exit or capital-preservation review.

Momentum Setup is a bull-phase continuation/re-entry family, not the same thing as classical MACD crossover transition.

The actual production signal engine/stage evaluators are not yet complete.

## Completed Groundwork

Documentation and architecture:

- Fresh program charter.
- V2 gap analysis against the fresh charter.
- V3 initial analysis and way-forward plan.
- V3 module contracts.
- V3 evidence-to-stage matrix.
- V3 baseline decision tree.
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
- CSV universe loader with metadata preservation for mixed NSE/BSE/NYSE/NASDAQ files.
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
- First production Crossover evaluator slice.
- Daily evidence builder for MACD, RSI, ADX, Bollinger, EMA, volume, and price structure.
- Crossover route classifier focused on bull/bear phase transition.
- Direction-aware Crossover scoring for bull transition entry signals and bear transition exit/preservation signals.
- Dedicated Momentum Setup evaluator for bull-phase pullback re-entry and continuation candidates.
- Stage-family dispatcher that can evaluate Crossover, Momentum Setup, or both from a shared evidence pack.
- Baseline router that classifies market, sector, and stock regimes before stage-family selection.
- Configurable regime benchmark mapping for exchanges, geographies, sectors, and themes.
- Non-fatal benchmark loading into `PriceDataBundle.benchmarks` for market/sector regime classification.
- Positive-elimination guardrail that blocks bullish entry/Momentum Setup when market, sector, and stock are all bearish, while preserving bear Crossover exit review.
- CLI/run parameter support for comma-separated stage families.
- Reusable run orchestrator.
- CLI entry point.
- Initial Python web UI wrapper.
- Backtest outcome classification for candidate follow-through.
- Failure-category summary reporting for failed candidate follow-through.
- Candidate score-bucket summary reporting.

Tests:

- Universe loader tests.
- Backtesting utility tests.
- Backtest engine tests.
- Data provider tests.
- Report/output contract tests, including score-bucket and failure-category summaries.
- Stage evaluator tests for Crossover transition, Momentum Setup re-entry/continuation, and family dispatch.
- Baseline router tests for market/sector/stock positive elimination and bearish Crossover preservation.
- Regime benchmark configuration tests.
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
- `src/stock_screener_v3/indicators.py`
- `src/stock_screener_v3/evidence.py`
- `src/stock_screener_v3/evaluators.py`
- `src/stock_screener_v3/runner.py`
- `src/stock_screener_v3/cli.py`
- `web_app_v3.py`

Key docs:

- `docs/charter/engine_program_charter_fresh_2026-06-01.md`
- `docs/analysis/current_engine_gap_analysis_against_fresh_charter_2026-06-01.md`
- `docs/analysis/v3_initial_engine_analysis_and_way_forward_2026-06-01.md`
- `docs/architecture/v3_module_contracts.md`
- `docs/architecture/v3_evidence_stage_matrix.md`
- `docs/architecture/v3_baseline_decision_tree.md`
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
6df0f7e Mark regime engine v1 complete
f635e3d Add configurable regime benchmarks
d9dc18d Add baseline regime router
b915718 Add V3 evidence stage matrix
faf5398 Add momentum setup stage evaluator
bd5d782 Add bear transition crossover route
bd693ac Split crossover route opportunity states
2dc2e6f Add backtest failure category reporting
021c9e0 Support mixed exchange universe inputs
4e4dcce Add first V3 crossover engine slice
```

## What Is Not Yet Built

The actual V3 production engine logic has started but is not complete yet:

- Crossover v1 exists, but it is a first slice and needs historical calibration.
- Crossover is direction-aware for bull/bear transition.
- Momentum Setup v1 exists for bull pullback re-entry and bull continuation, but still needs calibration.
- Market/sector/stock regime determination v1 is complete for the current engine layer:
  - configurable benchmark mappings exist in `RegimeBenchmarkConfig`;
  - benchmark loading is wired through the backtest engine;
  - benchmark failures degrade to `UNKNOWN` instead of skipping the stock;
  - market, sector, and stock regimes are emitted in the output CSV.
- Remaining regime-engine expansion is configuration ergonomics and coverage, not core architecture:
  - user-editable mapping file or config loader;
  - broader NSE/BSE sector-index mapping;
  - theme benchmark mapping conventions;
  - calibrated regime thresholds after validation.
- Failure categories are first-pass diagnostics and still need validation against broader historical runs.
- No production Divergence evaluator.
- No scoring calibration beyond data model contracts.
- V3 web UI exists only as an initial Python wrapper.
- CLI exists for single-date backtest execution.

## Recommended Next Session Start

Start with the lower-level stock traversal path layer, not UI expansion and not new indicator tuning.

Recommended next implementation order:

1. Add an explicit `StockTraversalPlan` or equivalent route object between `BaselineDecision` and family evaluators.
2. Move allowed/blocked family and direction decisions into that route object while preserving current behavior.
3. Emit route diagnostics even when the final state is `STATUS_QUO`.
4. Use `docs/architecture/v3_baseline_decision_tree.md` and `docs/architecture/v3_evidence_stage_matrix.md` as the governing maps before adding or changing stage rules.
5. Add Divergence only after traversal and ranking contracts are stable.

## Carry-Forward Rules

- Do not hide technical signal validity because of quality/context concerns. Use `CandidateClass`, `ReviewPriority`, and risk tags instead.
- Do not tune a rule from one stock/event.
- Do not promote signal-rule changes without a backtest report.
- Preserve sector/exchange metadata from the input universe in output rows.
- Accept mixed-market CSV inputs with NSE, BSE, NYSE, and NASDAQ codes.
- Normalize NSE symbols to `.NS` and BSE symbols to `.BO`; keep NYSE/NASDAQ unsuffixed unless `YahooSymbol` is provided.
- Preserve V2-compatible offline CSV headers.
- Keep log, output CSV, and summary report separate.
- Keep the handover document updated after every meaningful change.
