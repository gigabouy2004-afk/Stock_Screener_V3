# Stock Screener V3 Handover

Last updated: 2026-06-07

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
- Python scanner console for user-selected V3 scans with visible stage classifications and V2-style diagnostics.
- Backtest outcome classification for candidate follow-through.
- Failure-category summary reporting for failed candidate follow-through.
- Candidate score-bucket summary reporting.
- Average and median forward-return summary reporting.
- Score-bucket, sector, and review-priority outcome breakdowns for calibration.
- Stage-family outcome breakdowns for calibration.
- Risk-tag outcome breakdowns for calibration.
- Ranking collision bucket reporting in single-date and multi-date summaries.
- Multi-date backtest pack runner and CLI command.
- Web app support for user-facing scan runs using the shared V3 runner path.
- Web UI stage classification cards for `PRE_BULL_CROSSOVER`, `PRE_BEAR_CROSSOVER`, Divergence states, Momentum Setup states, and `STATUS_QUO`.

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
- Web UI stage-classification correction smoke, not committed as artifacts:
  - command label: `v3_ui_stage_http_smoke`
  - confirmed initial page shows stage taxonomy
  - confirmed result table includes V2-visible diagnostic fields such as `CandidateStateRaw`, `MACD_1D_CrossoverState`, and `RSI_1D`
- Web UI scanner-framing correction:
  - removed visible backtest/multi-date pack controls from the operator UI
  - retained D as the scan/as-of date used by the shared V3 execution path
  - backtesting remains a CLI/validation harness, not the primary web UI model

## 2026-06-05 Validation Checkpoint

Full Technology-universe validation started from:

- `data/samples/00-NYSE_NASDAQ_Common_Stocks_Sector-Technology.csv`
- 525 NYSE/NASDAQ Technology symbols attempted per date
- stage families: `CROSSOVER,MOMENTUM_SETUP,DIVERGENCE`
- forward horizons: D+1, D+2, D+5, D+10, D+20

The initial full `backtest-pack` command completed all three per-date runs but hit the shell timeout before writing the built-in aggregate markdown. The completed date artifacts were preserved, and a manual aggregate summary was written from the per-date detail CSVs:

- `validation/runs/v3_tech_full_pack_20260605_20260211_summary.md`
- `validation/runs/v3_tech_full_pack_20260605_20260311_summary.md`
- `validation/runs/v3_tech_full_pack_20260605_20260411_summary.md`
- `validation/runs/v3_tech_full_pack_20260605_aggregate_summary.md`
- `validation/runs/v3_tech_full_pack_20260605_calibration_review.md`
- `validation/runs/v3_tech_weak_watch_priority_review_20260605.md`
- `validation/runs/v3_nontech_master_watch_probe_20260605_20260211_summary.md`
- `validation/runs/v3_nontech_master_watch_probe_20260605_20260311_summary.md`
- `validation/runs/v3_nontech_master_watch_probe_20260605_multi_date_summary.md`
- `validation/runs/v3_nontech_master_watch_probe_20260605_review.md`
- `validation/runs/v3_usa_folder_nontech_watch_probe_20260605_20260211_summary.md`
- `validation/runs/v3_usa_folder_nontech_watch_probe_20260605_20260311_summary.md`
- `validation/runs/v3_usa_folder_nontech_watch_probe_20260605_multi_date_summary.md`
- `validation/runs/v3_usa_folder_nontech_watch_probe_20260605_review.md`

Per-date results:

| D date | Symbols processed | Symbols skipped | Candidates | Candidate density |
|---|---:|---:|---:|---:|
| 2026-02-11 | 512 | 13 | 354 | 0.6914 |
| 2026-03-11 | 514 | 11 | 354 | 0.6887 |
| 2026-04-11 | 514 | 11 | 450 | 0.8755 |

Aggregate candidate outcomes across 1,158 candidates:

| Horizon | Evaluated | Positive | Hit Rate | Average Return | Median Return |
|---|---:|---:|---:|---:|---:|
| D+1 | 1158 | 531 | 45.85% | 0.19% | -0.27% |
| D+2 | 1158 | 595 | 51.38% | 0.98% | 0.16% |
| D+5 | 1158 | 662 | 57.17% | 3.39% | 1.31% |
| D+10 | 1158 | 668 | 57.69% | 5.15% | 2.39% |
| D+20 | 1158 | 619 | 53.45% | 8.86% | 1.56% |

Candidate family mix:

| D date | CROSSOVER | MOMENTUM_SETUP | DIVERGENCE |
|---|---:|---:|---:|
| 2026-02-11 | 153 | 82 | 119 |
| 2026-03-11 | 104 | 83 | 167 |
| 2026-04-11 | 162 | 174 | 114 |

Diagnostic confirmation:

- all processed rows in all three detail CSVs include ranking diagnostics;
- all processed rows include traversal diagnostics;
- all processed rows include Divergence diagnostic fields;
- `MOMENTUM_SETUP` was blocked when stock baseline was bearish while bearish `CROSSOVER` remained available;
- `DIVERGENCE` meaningfully competed for the winning family, especially on 2026-03-11.

Initial calibration read:

- February and March Technology runs had high candidate density but weak forward outcomes.
- April Technology behavior was broadly strong and heavily lifted the aggregate result.
- Active-family collision buckets confirmed that ranking makes real choices among competing stage-family interpretations, not just cosmetic ordering.
- `WATCH` and `NEEDS_MANUAL_REVIEW` are not yet reliable weakness separators by themselves:
  - February `WATCH` D+20: 97 candidates, 40.21% hit rate, 1.36% average return.
  - March `WATCH` D+20: 197 candidates, 23.86% hit rate, -3.34% average return.
- The clearest weak-date discriminator is `WATCH + BELOW_EMA200`, especially bullish Divergence and Momentum Setup:
  - March `WATCH + BELOW_EMA200` D+20: 102 candidates, 10.78% hit rate, -8.89% average return.
  - March `DIVERGENCE + BULLISH_DIVERGENCE + BELOW_EMA200` D+20: 52 candidates, 11.54% hit rate, -6.64% average return.
  - March `MOMENTUM_SETUP + BULL_PULLBACK_REENTRY + BELOW_EMA200` D+20: 37 candidates, 10.81% hit rate, -12.60% average return.
- Automatic summary reporting now includes `Stage Family Outcomes`, `Risk Tag Outcomes`, and `Ranking Collision Buckets`.
- Larger non-Technology validation from `D:\Tools\StockCodeMaster\Script\NYSE_NASDAQ_Master_Library.csv` was run using a derived 5,535-row non-Technology common-stock universe:
  - derived file: `data/samples/us_non_technology_master_sample_20260605.csv`;
  - run label: `v3_nontech_master_watch_probe_20260605`;
  - sample size: 200, random seed: 20260605;
  - February processed 186 symbols, found 150 candidates;
  - March processed 186 symbols, found 126 candidates;
  - February `WATCH + BELOW_EMA200` D+20: 20 candidates, 25.00% hit rate, -8.29% average return;
  - March `WATCH + BELOW_EMA200` D+20: 17 candidates, 41.18% hit rate, -9.12% average return;
  - March `MOMENTUM_SETUP / BULL_PULLBACK_REENTRY + BELOW_EMA200` D+20: 6 candidates, 33.33% hit rate, -16.79% average return.
- USA-folder sector validation was run from `D:\Tools\StockCodeMaster\USA`:
  - derived file: `data/samples/us_usa_folder_nontech_sector_universe_20260605.csv`;
  - run label: `v3_usa_folder_nontech_watch_probe_20260605`;
  - source files: Basic Materials, Energy, Industrial, Misc, Telecom, and Utilities;
  - sample size: 200, random seed: 20260605;
  - February processed 191 symbols, found 163 candidates;
  - March processed 193 symbols, found 152 candidates;
  - February `WATCH + BELOW_EMA200` D+20: 11 candidates, 27.27% hit rate, -0.12% average return;
  - March `WATCH + BELOW_EMA200` D+20: 19 candidates, 57.89% hit rate, 5.88% average return;
  - this does not confirm generic March `WATCH + BELOW_EMA200` weakness for USA-folder sectors.
- This is a first promoted validation baseline, not a rule-tuning justification. More dates and sectors are required before changing thresholds.

Reporting smoke after the calibration review:

- command label: `v3_collision_report_smoke`
- sample: `data\samples\us_master_sample.csv`
- dates: `2026-02-11,2026-03-11`
- confirmed single-date summaries include `Stage Family Outcomes` and `Ranking Collision Buckets`;
- confirmed multi-date summary includes `Ranking Collision Buckets`.
- command label: `v3_risk_tag_report_smoke`
- confirmed single-date summaries include `Risk Tag Outcomes`.

Last verification before restart:

```text
python -m unittest discover -s tests -v
58 tests passing
```

## 2026-06-07 Sector-Folder Validation Checkpoint

Resumed from the 2026-06-05 handover and ran the recommended sector-by-sector validation packs from `D:\Tools\StockCodeMaster\USA`.

Validation command shape:

```powershell
$env:PYTHONPATH='D:\Tools\Stock_Screener_V3\src'
python -m stock_screener_v3.cli backtest-pack --workspace-root . --universe-file <sector-file> --d-dates 2026-02-11,2026-03-11,2026-04-11 --forward-days 1,2,5,10,20 --stage-family CROSSOVER,MOMENTUM_SETUP,DIVERGENCE --run-label <sector-label>
```

Sector files copied into `data/samples`:

- `00-NYSE_NASDAQ_Common_Stocks_Sector-BasicMaterials.csv`
- `00-NYSE_NASDAQ_Common_Stocks_Sector-Energy.csv`
- `00-NYSE_NASDAQ_Common_Stocks_Sector-Industrial.csv`
- `00-NYSE_NASDAQ_Common_Stocks_Sector-Misc.csv`
- `00-NYSE_NASDAQ_Common_Stocks_Sector-Telecom.csv`
- `00-NYSE_NASDAQ_Common_Stocks_Sector-Utilities.csv`
- `00-NYSE_NASDAQ_Common_Stocks_Sector-Technology-Semiconductor.csv`

New review artifact:

- `validation/runs/v3_sector_folder_validation_review_20260607.md`
- `validation/runs/v3_cross_sector_calibration_review_20260607.md`

Aggregate summaries:

- `validation/runs/v3_sector_basic_materials_pack_20260607_multi_date_summary.md`
- `validation/runs/v3_sector_energy_pack_20260607_multi_date_summary.md`
- `validation/runs/v3_sector_industrial_pack_20260607_multi_date_summary.md`
- `validation/runs/v3_sector_misc_pack_20260607_multi_date_summary.md`
- `validation/runs/v3_sector_telecom_pack_20260607_multi_date_summary.md`
- `validation/runs/v3_sector_utilities_pack_20260607_multi_date_summary.md`
- `validation/runs/v3_sector_technology_semiconductor_pack_20260607_multi_date_summary.md`

Candidate outcomes, where candidates mean `SELECTED` plus `WATCH`:

| Sector | Processed | Candidates | Density | D+20 Hit Rate | D+20 Average | D+20 Median |
|---|---:|---:|---:|---:|---:|---:|
| Basic Materials | 361 | 285 | 0.7895 | 32.98% | -3.23% | -4.49% |
| Energy | 402 | 358 | 0.8905 | 60.89% | 4.10% | 2.53% |
| Industrial | 1370 | 1140 | 0.8321 | 48.51% | 0.74% | -0.43% |
| Misc | 194 | 146 | 0.7526 | 41.10% | -1.83% | -3.08% |
| Telecom | 191 | 161 | 0.8429 | 50.31% | 3.64% | 0.01% |
| Utilities | 366 | 331 | 0.9044 | 52.87% | 0.66% | 0.49% |
| Technology Semiconductor | 255 | 189 | 0.7412 | 58.20% | 18.11% | 8.69% |

Calibration read:

- Candidate density remains high across all sector-folder packs.
- Basic Materials and Misc were weak at D+20.
- Energy and Technology Semiconductor were strongest at D+20, though Semiconductor was heavily lifted by April 2026.
- Industrial and Utilities were date-sensitive rather than uniformly strong or weak.
- `WATCH + BELOW_EMA200` did not reproduce as a generic weak filter in these sector-folder runs.
- Cross-sector review confirmed that date regime dominates several sectors and that family behavior is sector-specific.
- No scoring or threshold changes were made from this validation pass.

Follow-up symbol-level review:

- `validation/runs/v3_symbol_level_failure_review_20260607.md`
- Basic Materials Crossover D+20 remained weak:
  - 94 candidates, 21.28% hit rate, -7.79% average return, -8.20% median return;
  - weakness was concentrated in February and March;
  - `PRE_BEAR_CROSSOVER` was worse than `PRE_BULL_CROSSOVER`, which reinforces that bearish Crossover should be interpreted as exit/capital-preservation visibility, not bullish-entry quality.
- The Basic Materials sector file uses `Basic Materials`, but the default regime config only mapped `MATERIALS` to `XLB`.
- Added `BASIC MATERIALS -> XLB` to `RegimeBenchmarkConfig.default()` and added a regression test.
- Reran Basic Materials with run label `v3_sector_basic_materials_regime_alias_check_20260607`:
  - processed 361 rows across three dates;
  - found 285 candidates;
  - sector regimes changed from all `UNKNOWN` to 241 `BULLISH` and 120 `MIXED`;
  - candidate counts and outcomes were unchanged, confirming the Crossover weakness was not only a missing-sector-context artifact.
- Misc Divergence D+20 remained weak:
  - 52 candidates, 34.62% hit rate, -1.24% average return, -4.05% median return;
  - hidden and bullish variants were weaker, but more dates are needed before changing Divergence thresholds.

Bear Crossover drawdown review:

- `validation/runs/v3_basic_materials_bear_crossover_drawdown_review_20260607.md`
- Added path-aware forward validation detail columns:
  - `DPlus{N}WorstLowReturnPct`;
  - `DPlus{N}BestHighReturnPct`.
- These columns are additive and do not change existing endpoint-return summaries.
- Reran Basic Materials with run label `v3_basic_materials_path_metrics_20260607`.
- Basic Materials `PRE_BEAR_CROSSOVER` D+20 path result:
  - 50 candidates;
  - endpoint average -10.14%, endpoint median -10.86%;
  - worst-low average -23.00%, worst-low median -25.36%;
  - 86.00% had a D+20 worst-low drawdown of at least 10%.
- March 2026 `PRE_BEAR_CROSSOVER` was the clearest exit-review window:
  - 32 candidates;
  - D+20 worst-low average -26.00%;
  - D+20 worst-low median -27.22%.
- Interpretation: `PRE_BEAR_CROSSOVER` should remain visible as exit/capital-preservation review, not be scored as bullish-entry quality.

Verification after restart:

```text
python -m unittest discover -s tests -v
60 tests passing
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
- Multi-date backtest pack exists, the first Technology full-universe validation baseline is documented, and the 2026-06-07 USA sector-folder validation baseline is documented.
- Divergence v1 is now part of the default holistic stage-family set, but swing geometry and thresholds still need historical calibration.
- No scoring calibration beyond data model contracts.
- Enriched NYSE/NASDAQ master universe CSV is not complete yet. This parallel WIP should populate universe filter/cache fields such as `CompanyName`, `MarketCap`, P/E fields, dividend dates, earnings date, beta, shares/float, and volume/profile metadata so scans can run on narrower symbol sets instead of always using `ALL_CODES`.
- V3 web app is operational for local scan execution, but deeper UI ergonomics can remain on hold while engine calibration proceeds.
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

1. Add summary reporting for forward worst-low and best-high metrics by stage family and candidate state.
2. Compare `PRE_BEAR_CROSSOVER` drawdown behavior across Energy, Industrial, Technology, Utilities, and Telecom before changing review priority.
3. In the live scanner UI, visually separate `PRE_BEAR_CROSSOVER` as exit/capital-preservation review from bullish-entry candidates.
4. Add generated cross-sector and symbol-level calibration report commands once the manual review formats stabilize.

Parallel WIP track:

1. Define the enriched NYSE/NASDAQ master universe CSV schema.
2. Add or revive the metadata enrichment workflow for company/profile/financial filter fields.
3. Add universe pre-filter support for predicates such as `TrailingPE < 25`, market-cap ranges, dividend yield, beta, average volume, sector, and industry.
4. Preserve enriched fields for filtering, output, and UI detail use without treating current profile metadata as historical signal truth.
5. Add loader/filter/output tests for required enriched metadata fields.

Current external code-list source rule:

- Use `D:\Tools\StockCodeMaster\USA` for sector-folder validation and sector-specific code lists.
- Use `D:\Tools\StockCodeMaster\Script\NYSE_NASDAQ_Master_Library.csv` when a broad all-sector NYSE/NASDAQ common-stock universe is required.
- The `USA` folder currently has full-schema sector files for Basic Materials, Energy, Industrial, Misc, Technology, Telecom, and Utilities, plus smaller symbol-only theme/subsector files.

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
