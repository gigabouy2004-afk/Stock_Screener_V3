# Stock Screener V3 Handover

Last updated: 2026-06-04

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `main`

Latest confirmed local and pushed code baseline: current `main` after the backtesting expansion checkpoint.

Local `main` and `origin/main` should be verified in sync at restart with `git status --short --branch`.

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
58 tests passing
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
- V3 Divergence contract.
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
- Baseline universe metadata contract for enriched NYSE/NASDAQ master universe fields.
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
- Dedicated Divergence evaluator for regular and hidden bullish/bearish divergence candidates.
- Stage-family dispatcher that can evaluate Crossover, Momentum Setup, Divergence, or selected subsets from a shared evidence pack.
- Baseline router that classifies market, sector, and stock regimes before stage-family selection.
- Configurable regime benchmark mapping for exchanges, geographies, sectors, and themes.
- Non-fatal benchmark loading into `PriceDataBundle.benchmarks` for market/sector regime classification.
- Positive-elimination guardrail that blocks bullish entry/Momentum Setup when market, sector, and stock are all bearish, while preserving bear Crossover exit review.
- Explicit `StockTraversalPlan` route object between `BaselineDecision` and stage-family evaluators.
- Traversal diagnostics for selected families, evaluable families, blocked families, and traversal route reason.
- Divergence diagnostics for route candidate, price/momentum swing, confirmation state, direction, type, opportunity, quality components, and reason codes.
- Formal V3 ranking contract for choosing the reported `StageEvaluation` after multi-family traversal.
- Ranking diagnostics for winning rows: contract version, rule, winner family, evaluated families, candidate states/classes, priorities, and scores.
- Divergence included in the default holistic stage-family set after ranking diagnostics were made explicit.
- Divergence direction now participates in baseline bullish-route blocking, matching Crossover and Momentum Setup traversal behavior.
- CLI/run parameter support for comma-separated stage families.
- Reusable run orchestrator.
- CLI entry point.
- Python web console for single-date and multi-date V3 runs.
- Backtest outcome classification for candidate follow-through.
- Failure-category summary reporting for failed candidate follow-through.
- Candidate score-bucket summary reporting.
- Average and median forward-return summary reporting.
- Score-bucket, sector, and review-priority outcome breakdowns for calibration.
- Multi-date backtest pack runner and CLI command.
- Web app support for single-date and multi-date runs using the shared V3 runner path.

Tests:

- Universe loader tests.
- Backtesting utility tests.
- Backtest engine tests.
- Data provider tests.
- Report/output contract tests, including score-bucket and failure-category summaries.
- Stage evaluator tests for Crossover transition, Momentum Setup re-entry/continuation, and family dispatch.
- Divergence evaluator tests for regular bullish, regular bearish, hidden bullish, hidden bearish, status quo, and stage-family dispatch.
- Baseline router tests for market/sector/stock positive elimination and bearish Crossover preservation.
- Stock traversal plan tests for family blocking, user family restriction preservation, aliases, and status-quo diagnostics.
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
- `docs/architecture/v3_divergence_contract.md`
- `docs/architecture/v3_ranking_contract.md`
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

## Last Pushed Restart Snapshot

This session checkpoint has been committed and pushed to GitHub.

Pushed checkpoint:

Backtesting expansion checkpoint after `f8daec9 Close V3 ranking and divergence default path`.

Implemented in this checkpoint:

- Explicit `StockTraversalPlan` route object and traversal diagnostics.
- Divergence contract document.
- Divergence v1 evaluator and diagnostics for regular/hidden bullish/bearish divergence.
- Output contract additions for traversal and Divergence diagnostics.
- Focused tests for traversal and Divergence.
- Formal ranking contract and winning-row ranking diagnostics.
- Default holistic traversal with `CROSSOVER,MOMENTUM_SETUP,DIVERGENCE`.
- Backtesting documentation update for the full V3 execution path.
- Multi-date backtest pack command and aggregate summary.
- Average/median forward returns plus score-bucket, sector, and review-priority outcomes.
- Parallel architecture track for enriched NYSE/NASDAQ master-universe filter fields.
- Smoke summaries:
  - `validation/runs/v3_traversal_plan_smoke_20260211_summary.md`
  - `validation/runs/v3_divergence_smoke_20260211_summary.md`
- Live full-engine smoke, not committed as an artifact:
  - command label: `v3_full_engine_live_smoke`
  - D date: `2026-02-11`
  - stage families: `CROSSOVER,MOMENTUM_SETUP,DIVERGENCE`
  - sample: `data\samples\us_master_sample.csv`
  - processed 3 symbols, skipped 0, found 2 candidates
  - CSV confirmed traversal, ranking, and Divergence diagnostic columns
- Live multi-date pack smoke, not committed as an artifact:
  - command label: `v3_pack_live_smoke`
  - D dates: `2026-02-11,2026-03-11`
  - stage families: `CROSSOVER,MOMENTUM_SETUP,DIVERGENCE`
  - sample: `data\samples\us_master_sample.csv`
  - processed 6 symbol-date rows, skipped 0, found 3 candidates
  - aggregate summary confirmed per-date density and aggregate D+1/D+2/D+5 outcomes
- Web app HTTP smoke, not committed as artifacts:
  - URL: `http://127.0.0.1:8010`
  - single-date web POST used `v3_web_http_smoke`
  - multi-date web POST used `v3_web_pack_http_smoke`
  - both returned rendered result summaries and artifact paths

Last verification before restart:

```text
python -m unittest discover -s tests -v
58 tests passing
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
- Multi-date backtest pack exists, but promoted calibration baselines are not yet built.
- Divergence v1 is now part of the default holistic stage-family set, but swing geometry and thresholds still need historical calibration.
- No scoring calibration beyond data model contracts.
- Enriched NYSE/NASDAQ master universe CSV is not complete yet. This parallel WIP should populate universe filter/cache fields such as `CompanyName`, `MarketCap`, P/E fields, dividend dates, earnings date, beta, shares/float, and volume/profile metadata so scans can run on narrower symbol sets instead of always using `ALL_CODES`.
- V3 web app is operational for local single-date and multi-date execution, but deeper UI ergonomics can remain on hold while engine calibration proceeds.
- CLI exists for single-date backtest execution.

## Recommended Next Session Start

Start with ranking validation/backtest review and calibration planning, not UI expansion and not new indicator tuning.

Current traversal layer status:

- `StockTraversalPlan` exists in `src/stock_screener_v3/baseline_router.py`.
- `StageFamilyEvaluator` now builds a traversal plan before dispatching family evaluators.
- Current behavior is preserved:
  - all-bearish context blocks bullish entry;
  - all-bearish context blocks `MOMENTUM_SETUP`;
  - bearish `CROSSOVER` remains available for exit/capital-preservation review;
  - user-selected family restrictions and aliases are preserved;
- traversal diagnostics are emitted for selected, blocked, and `STATUS_QUO` outputs.
- ranking diagnostics are emitted on the winning reported row.
- default holistic traversal now evaluates `CROSSOVER`, `MOMENTUM_SETUP`, and `DIVERGENCE`.
- Smoke run `v3_traversal_plan_smoke` on 2026-02-11 processed 3 sample symbols, found 2 candidates, skipped 0 symbols, and emitted traversal diagnostics on selected and `STATUS_QUO` rows.
- Smoke run `v3_divergence_smoke` on 2026-02-11 used `--stage-family DIVERGENCE`, processed 3 sample symbols, found 0 candidates, skipped 0 symbols, and emitted Divergence diagnostics on `STATUS_QUO` rows.

Completed in the 2026-06-04 closure pass:

1. Defined the formal ranking contract beyond current best-`StageEvaluation` selection.
2. Added tests around ranking order, tie-break behavior, default Divergence dispatch, and bullish Divergence baseline blocking.
3. Included `DIVERGENCE` in the default holistic stage-family set after ranking diagnostics were explicit.

Recommended next implementation order:

1. Run broader live multi-date sample backtests with default `CROSSOVER,MOMENTUM_SETUP,DIVERGENCE`.
2. Review ranking diagnostics for cases where Divergence competes with Crossover or Momentum Setup.
3. Promote repeatable multi-date validation summaries as calibration baselines.
4. Start calibration notes from repeated historical runs; do not tune from a single stock/event.

Parallel WIP track:

1. Define the enriched NYSE/NASDAQ master universe CSV schema.
2. Add or revive the metadata enrichment workflow for company/profile/financial filter fields.
3. Add universe pre-filter support for predicates such as `TrailingPE < 25`, market-cap ranges, dividend yield, beta, average volume, sector, and industry.
4. Preserve enriched fields for filtering, output, and UI detail use without treating current profile metadata as historical signal truth.
5. Add loader/filter/output tests for required enriched metadata fields.

## Carry-Forward Rules

- Do not hide technical signal validity because of quality/context concerns. Use `CandidateClass`, `ReviewPriority`, and risk tags instead.
- Do not tune a rule from one stock/event.
- Do not promote signal-rule changes without a backtest report.
- Preserve sector/exchange metadata from the input universe in output rows.
- Use enriched master-universe metadata for pre-scan filters before price loading and stage evaluation.
- Prefer enriched master-universe metadata for UI detail panes before making live profile calls.
- Accept mixed-market CSV inputs with NSE, BSE, NYSE, and NASDAQ codes.
- Normalize NSE symbols to `.NS` and BSE symbols to `.BO`; keep NYSE/NASDAQ unsuffixed unless `YahooSymbol` is provided.
- Preserve V2-compatible offline CSV headers.
- Keep log, output CSV, and summary report separate.
- Keep the handover document updated after every meaningful change.
