# Stock Screener V3 Transition Signoff

Date: 2026-06-02

Repo: `D:\Tools\Stock_Screener_V3`

Remote: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `main`

Code baseline verified before shutdown: `9687742 Add traversal and divergence v1 engine layer`

Purpose: preserve enough technical and decision context to restart the V3 engine build after signoff without relying on chat history.

## 1. Restart Checklist

Run this first after signing in again:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -10
$env:PYTHONPATH='D:\Tools\Stock_Screener_V3\src'
python -m unittest discover -s tests -v
```

Expected repository state after restart:

```text
## main...origin/main
```

Expected tests:

```text
52 tests passing
```

Optional smoke run after restart:

```powershell
python -m stock_screener_v3.cli backtest --workspace-root D:\Tools\Stock_Screener_V3 --universe-file data\samples\us_master_sample.csv --d-date 2026-02-11 --forward-days 1,2,5 --run-label v3_restart_smoke
```

Benchmark-backed smoke runs use live/remote price loading and can vary if the data provider is unavailable. Unit tests are the stable restart check.

## 2. Cardinal Purpose Of V3

V3 is a clean rebuild of the stock screener engine. It should not become a tuned copy of the V2 Crossover monolith.

The engine must evaluate a stock holistically:

```text
UniverseRecord
-> PriceDataBundle
-> EvidencePack
-> BaselineDecision
-> stage-family traversal
-> StageEvaluation
-> output CSV, summary report, run log
```

Backtesting exists to validate and calibrate the engine. Backtesting is not the primary engine purpose.

The primary purpose is controlled stock traversal:

1. Establish market, sector, and stock baseline regimes.
2. Positively eliminate stage paths that do not make sense.
3. Send the stock only into applicable lower-level evaluators.
4. Preserve rejected/watch reasons instead of hiding signals.
5. Rank and report the best current candidate state with enough audit fields to explain the path.

## 3. Current Stage Nomenclature

These definitions are settled.

| Family | Candidate states | Purpose |
|---|---|---|
| `CROSSOVER` | `PRE_BULL_CROSSOVER`, `PRE_BEAR_CROSSOVER` | Phase transition. Bull transition is for new capital entry review. Bear transition is for exit or capital preservation review. |
| `MOMENTUM_SETUP` | `BULL_PULLBACK_REENTRY`, `BULL_CONTINUATION_MOMENTUM` | Bull phase continuation or re-entry after bullish conditions already exist. |
| `DIVERGENCE` | `BULLISH_DIVERGENCE`, `BEARISH_DIVERGENCE`, `HIDDEN_BULLISH_DIVERGENCE`, `HIDDEN_BEARISH_DIVERGENCE` | Price and momentum disagreement. V1 evaluator implemented for explicitly selected Divergence runs; calibration pending. |
| `STATUS_QUO` | `STATUS_QUO` | No selected family has sufficient route evidence. |

Momentum Setup is a bull-phase family. It is not the same thing as classical MACD Crossover transition.

Classical Crossover transition means momentum moving from seller to buyer control, or buyer to seller control. For V3:

- `PRE_BULL_CROSSOVER`: seller/neutral pressure transitioning toward buyer control.
- `PRE_BEAR_CROSSOVER`: buyer/neutral support transitioning toward seller control.

## 4. What Is Complete Now

The market regime determination layer is V1 complete for engine traversal.

Implemented:

- Configurable code-level benchmark mapping through `RegimeBenchmarkConfig`.
- Market benchmark selection by exchange/geography.
- Sector benchmark selection by sector.
- Theme benchmark mapping support.
- Benchmark loading through `BacktestEngine`.
- Per-run benchmark cache.
- Non-fatal benchmark failure behavior. Missing benchmark data becomes `UNKNOWN`; stock evaluation continues.
- Market, sector, and stock regime classification.
- Baseline positive elimination before selected stage-family evaluation.
- Explicit `StockTraversalPlan` routing layer between `BaselineDecision` and stage-family evaluation.
- Divergence family evaluator covering regular and hidden bullish/bearish divergence.
- Architecture/WIP track for enriched NYSE/NASDAQ master universe metadata to support pre-scan universe filters and reduce unnecessary profile fetch cycles.
- Output diagnostics for route visibility:
  - `MarketRegime`
  - `SectorRegime`
  - `StockRegime`
  - `AllowedBullishStages`
  - `AllowedBearishStages`
  - `BlockedStageFamilies`
  - `BaselineRouteReason`
  - `SelectedStageFamilies`
  - `TraversalCandidateFamilies`
  - `TraversalBlockedFamilies`
  - `TraversalRouteReason`
- Divergence diagnostics:
  - `DivergenceDirection`
  - `DivergenceType`
  - `DivergenceOpportunityType`
  - `DivergenceConfirmationState`
  - `DivergencePriceSwing`
  - `DivergenceMomentumSwing`
  - `DivergenceBarsAgo`
  - `DivergenceQualityScore`
  - `DivergenceQualityComponents`
  - `DivergenceReasonCodes`

Current default benchmark mappings include:

| Context | Benchmark |
|---|---|
| NASDAQ / Q | `QQQ` |
| NYSE / N | `SPY` |
| AMEX / A | `SPY` |
| NSE | `^NSEI` |
| BSE | `^BSESN` |
| Technology | `XLK` |
| Energy | `XLE` |
| Industrials | `XLI` |
| Financials | `XLF` |
| Health Care / Healthcare | `XLV` |
| Consumer Discretionary | `XLY` |
| Consumer Staples | `XLP` |
| Communication Services | `XLC` |
| Materials | `XLB` |
| Real Estate | `XLRE` |
| Utilities | `XLU` |

## 5. Current Module Ownership

Core source modules:

| File | Responsibility |
|---|---|
| `src/stock_screener_v3/models.py` | Shared dataclasses and enums. |
| `src/stock_screener_v3/universe.py` | Universe CSV loading, exchange normalization, metadata preservation. |
| `src/stock_screener_v3/data_provider.py` | Price provider interfaces and Yahoo wrapper. |
| `src/stock_screener_v3/indicators.py` | Neutral indicator calculations. |
| `src/stock_screener_v3/evidence.py` | Builds `EvidencePack` from prices and benchmarks. |
| `src/stock_screener_v3/baseline_router.py` | Regime classification and positive elimination. |
| `src/stock_screener_v3/regime_config.py` | Configurable benchmark mapping defaults and lookup methods. |
| `src/stock_screener_v3/evaluators.py` | Crossover, Momentum Setup, Divergence, and stage-family dispatcher. |
| `src/stock_screener_v3/backtest_engine.py` | Backtest orchestration, price loading, benchmark loading, forward outcomes. |
| `src/stock_screener_v3/runner.py` | Reusable run orchestration. |
| `src/stock_screener_v3/cli.py` | CLI entry point. |
| `src/stock_screener_v3/reports.py` | Detail CSV and summary markdown generation. |
| `src/stock_screener_v3/run_io.py` | Run artifact paths and logs. |
| `src/stock_screener_v3/output_contracts.py` | V2-compatible CSV header contract plus V3 additions. |

## 6. Current Flow In Code

Current implementation:

```text
StageFamilyEvaluator(stage_families=("CROSSOVER", "MOMENTUM_SETUP"))
-> build one EvidencePack
-> build BaselineDecision
-> build StockTraversalPlan
-> apply positive elimination through explicit traversal plan
-> evaluate remaining selected stage families
-> return the highest-ranked StageEvaluation
```

Current CLI default:

```text
--stage-family CROSSOVER,MOMENTUM_SETUP
```

Divergence can be run explicitly with:

```text
--stage-family DIVERGENCE
```

Positive elimination guardrail:

- If market, sector, and stock are all `BEARISH`, bullish entry paths are blocked.
- If stock baseline is bearish, `MOMENTUM_SETUP` is blocked.
- Bearish Crossover remains allowed because the same engine must support exit/capital preservation for already-invested capital.

## 7. Current Validation State

Unit tests cover:

- Universe loading and symbol normalization.
- Backtesting helpers and engine orchestration.
- Data provider behavior.
- Report/output contracts.
- Run I/O and artifact separation.
- Crossover evaluator.
- Momentum Setup evaluator.
- Divergence evaluator.
- Stage-family dispatch.
- Baseline router.
- Stock traversal planning.
- Regime benchmark configuration.

Last known full suite:

```text
52 tests passing
```

Important validation summaries:

- `validation/runs/v3_validation_smoke_20260211_summary.md`
- `validation/runs/v3_route_split_smoke_20260211_summary.md`
- `validation/runs/v3_bull_bear_crossover_smoke_20260211_summary.md`
- `validation/runs/v3_momentum_setup_smoke_20260211_summary.md`
- `validation/runs/v3_baseline_router_smoke_20260211_summary.md`
- `validation/runs/v3_regime_config_smoke_20260211_summary.md`
- `validation/runs/v3_traversal_plan_smoke_20260211_summary.md`
- `validation/runs/v3_divergence_smoke_20260211_summary.md`

Most generated CSV/log outputs are intentionally ignored by Git.

## 8. Important Architecture Docs

Read these in this order after restart:

1. `docs/handover/current_session_handover.md`
2. `docs/handover/transition_signoff_2026-06-02.md`
3. `docs/architecture/v3_baseline_decision_tree.md`
4. `docs/architecture/v3_evidence_stage_matrix.md`
5. `docs/architecture/v3_divergence_contract.md`
6. `docs/architecture/v3_module_contracts.md`
7. `docs/architecture/rebuild_way_forward_plan.md`
8. `docs/architecture/v2_operational_parity_contract.md`

The baseline decision tree and evidence stage matrix are the governing design documents for the next engine layer.

## 9. Known Gaps

These are not blockers for the current signoff, but they are not complete:

- Divergence v1 exists for explicitly selected `DIVERGENCE` runs, but swing geometry and thresholds still need historical calibration.
- Enriched NYSE/NASDAQ master universe CSV is not complete yet. It should include company/profile/financial filter fields such as `CompanyName`, `MarketCap`, P/E fields, dividend dates, earnings date, beta, shares/float, average-volume fields, and profile freshness metadata so scans can run on narrower symbol sets instead of always using `ALL_CODES`.
- No user-editable external benchmark mapping file yet.
- NSE/BSE sector-index mapping is still shallow.
- Theme benchmark conventions exist in config shape but are not integrated into CLI/user input.
- Lower timeframe 4H/1H trigger bridge is not wired.
- Ranking layer is only implicit through best `StageEvaluation` selection.
- Regime thresholds are V1 and need broader historical calibration.
- Web UI is an initial wrapper, not the main development target.

## 10. Next Development Step

After signoff/signin, do not jump directly into more indicator rules.

The lower-level stock traversal path layer now exists:

```text
EvidencePack
-> BaselineDecision
-> StockTraversalPlan
-> selected route candidates
-> family evaluators
-> ranked StageEvaluation
```

Traversal output rows have been smoke-validated on the sample universe. The next layer should make ranking more explicit before evaluator scoring is expanded.

Recommended next implementation:

1. Define the formal ranking contract beyond current best-`StageEvaluation` selection.
2. Add tests around ranking once that contract is settled.
3. Decide whether to include `DIVERGENCE` in the default holistic stage-family set after ranking diagnostics are explicit.

Only after ranking diagnostics are explicit should the engine proceed to default holistic Divergence dispatch or ranking calibration.

Parallel WIP track for baseline universe:

1. Define the enriched NYSE/NASDAQ master universe CSV schema.
2. Add or revive the metadata enrichment workflow for company/profile/financial filter fields.
3. Add universe pre-filter support for predicates such as `TrailingPE < 25`, market-cap ranges, dividend yield, beta, average volume, sector, and industry.
4. Preserve enriched metadata for scan output and UI detail panes to avoid unnecessary live profile fetches.
5. Keep profile/financial metadata tagged with source/freshness, and do not treat current metadata as historical truth in backtests unless explicitly marked.
6. Add tests proving enriched fields survive universe loading, filtering, and output/report generation.

## 11. Carry-Forward Guardrails

- Keep GitHub and local folder updated before moving to each next layer.
- Keep this handover trail updated after meaningful engine changes.
- Do not hide valid technical signals because context is weak. Classify them as `WATCH`, `REJECTED`, lower priority, or risk-tagged.
- Do not tune from one stock/event.
- Do not mix Crossover hard gates into Momentum Setup or Divergence.
- Do not use Momentum Setup conditions to suppress valid Crossover transition warnings.
- Keep evidence calculation neutral and separate from stage classification.
- Preserve V2-compatible CSV headers first, with V3 fields appended.
- Keep log, output CSV, and summary markdown as separate artifacts.
- Preserve mixed-market input support for NSE, BSE, NYSE, and NASDAQ.
- Normalize NSE to `.NS`, BSE to `.BO`, and keep US symbols unsuffixed unless `YahooSymbol` is provided.

## 12. Recent Commit Trace At Signoff Preparation

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

## 13. Last Pushed Restart Snapshot

This session checkpoint has been committed and pushed to GitHub.

Pushed checkpoint:

```text
9687742 Add traversal and divergence v1 engine layer
```

Implemented in this checkpoint:

- Explicit `StockTraversalPlan` route object and traversal diagnostics.
- Divergence contract document.
- Divergence v1 evaluator and diagnostics for regular/hidden bullish/bearish divergence.
- Output contract additions for traversal and Divergence diagnostics.
- Focused tests for traversal and Divergence.
- Parallel architecture track for enriched NYSE/NASDAQ master-universe filter fields.
- Smoke summaries:
  - `validation/runs/v3_traversal_plan_smoke_20260211_summary.md`
  - `validation/runs/v3_divergence_smoke_20260211_summary.md`

Last verification before restart:

```text
python -m unittest discover -s tests -v
52 tests passing
```
