# Stock Screener V3 Original Intent And Handover

Last updated: 2026-06-13

Repo: `D:\Tools\Stock_Screener_V3`

Branch: `main`

## Document Authority

This document is the canonical source of truth for Stock Screener V3's original intent.

The top-level purpose, user workflow, allowed analysis paths, V2 level architecture, data method, backtesting requirement, and non-goals in this document must not be changed by a future session without explicit user approval.

Future sessions may add implementation status, UI details, test status, and granular next steps, but they must not change the original direction recorded here.

Every new session must read this document before reading validation notes, calibration runs, handover summaries, or recent commits.

## Original Intent

V3 is a CSV-based, user-directed stock analysis engine.

The purpose of V3 is to preserve the useful V2 analysis logic while rebuilding it into a single cohesive structure that avoids the logical regressions that appeared when separate V2 paths were merged.

V3 is not a new broad market research project. It is not a pan-USA screening engine unless the user supplies a pan-USA CSV and explicitly asks for that processing. It is not a sector, regime, or macro calibration project by default.

The engine must process stocks from a user-provided CSV and produce analysis only for the user-selected processing path or paths.

## User Workflow Contract

The user workflow is fixed:

1. User provides a CSV file containing stock symbols or stock rows.
2. User selects the required analysis path or paths.
3. User provides the analysis date context where required.
4. Engine processes each stock through the structured V3 pipeline.
5. Engine produces explainable output, reason codes, diagnostics, and backtest/self-validation where applicable.

The only allowed user-facing analysis options are:

- `CROSSOVER`
- `DIVERGENCE`
- `MOMENTUM_SETUP` / `BULL_EXTENSION`

No hidden fourth path should be added. No sector, market-regime, ETF, or universe-expansion path should be treated as part of the core engine unless the user explicitly requests that as a separate feature.

## Three Analysis Paths

### Crossover

Crossover is for phase-transition analysis. It identifies setup conditions around bullish or bearish crossover events.

Valid examples:

- `PRE_BULL_CROSSOVER`
- `PRE_BEAR_CROSSOVER`
- confirmed bullish crossover
- confirmed bearish crossover

Crossover must not classify an already-extended bull continuation as `PRE_BULL_CROSSOVER`.

If MACD is already above the zero line and the evidence describes continuation or re-entry, the engine must route the stock to Momentum Setup / Bull Extension logic, not Crossover transition logic.

### Divergence

Divergence is for price-versus-indicator disagreement.

It must remain independent from Crossover and Momentum Setup logic. A divergence candidate must be identified through divergence-specific evidence, not through side effects of crossover or momentum rules.

The divergence path must preserve the V2 intent of finding meaningful bullish or bearish disagreement and then validating whether the signal had forward price behavior.

### Momentum Setup / Bull Extension

Momentum Setup / Bull Extension is for bull-phase continuation, re-entry, pullback recovery, and extension behavior.

This path handles stocks where the trend or MACD structure is already in a bullish continuation state. It is not the same as a fresh bullish crossover transition.

Examples of this path include:

- pullback re-entry
- bull extension
- continuation after MACD is already positive
- setups where price movement is expected after an already-established bullish structure

## V2 Level Architecture To Preserve

V3 must retain the path-first V2 architecture and make it stricter.

The V2 artifacts describe the core model as:

```text
L1 baseline -> L2 stage router -> L3 indicator functions
```

V3 should extend this into a complete implementation pipeline without changing that core meaning:

### L0 Input, Data, And Date Preparation

L0 prepares the run before analysis starts.

Responsibilities:

- load user CSV
- normalize symbols
- validate required columns
- resolve exchange/provider symbol format
- prepare D-date analysis context
- fetch or load required historical OHLCV data
- enforce no-lookahead data slicing for production classification
- record provider/data failures per symbol

### L1 Baseline

L1 establishes the stock's current technical state before any final stage classification.

Responsibilities:

- determine current trend state
- determine current MACD state
- determine moving-average context
- determine price structure and volume context where needed
- produce neutral baseline facts

L1 is not the final stage. It only establishes the current technical condition and gives L2 enough information to route safely.

### L2 Stage Router

L2 chooses the eligible path based on:

- user-selected analysis option
- L1 baseline state
- hard path boundaries

L2 must prevent path leakage.

Examples:

- a continuation state must not be routed as a fresh crossover transition
- divergence logic must not run because crossover logic failed
- momentum continuation must not be mixed with pre-crossover classification

### L3 Indicator And Evidence Functions

L3 calculates detailed evidence only for the path requested by L2.

Responsibilities:

- calculate indicators on demand
- return raw values and derived evidence
- avoid global indicator interpretation before the path is chosen
- keep Crossover, Divergence, and Momentum evidence independent

### L4 Classification And Scoring

L4 converts routed evidence into the final candidate class.

Responsibilities:

- apply path-specific thresholds
- assign candidate class
- assign confidence or priority
- produce reason codes
- reject logically inconsistent candidates

### L5 Output, Audit, And Backtest

L5 writes user-facing and developer-facing evidence.

Responsibilities:

- output CSV results
- output summary markdown/logs where required
- include L0/L1/L2/L3/L4 diagnostics
- perform D+X forward validation where requested or required
- preserve enough audit detail to debug why a symbol was classified or rejected

## API And Data Provider Method

The engine must use a provider abstraction rather than letting provider behavior leak into strategy logic.

Current implementation work has used a Yahoo/yfinance-style provider wrapper in the repository. That is an implementation detail, not the product identity of V3.

The required data-provider contract is:

- daily OHLCV history for the D-date window
- enough historical depth for indicators used by the selected path
- forward OHLCV bars for D+X self-backtesting
- deterministic slicing so classification uses only data available as of D
- per-symbol failure handling
- clear handling for missing dates, holidays, suspended symbols, provider gaps, and insufficient bars
- cache or reuse behavior that does not change analysis semantics
- rate-limit and provider-error reporting

If a future TradingView API or another market-data API is used, it must be integrated behind this provider contract. The analysis engine should not be rewritten around the provider.

Live mode and historical/backtest mode must use the same logical data contract. The only difference should be the date window and whether forward D+X bars are available for validation.

## Date Processing And D+X Self-Backtesting

Date processing is part of the core engine, not an optional later feature.

Definitions:

- `D`: the analysis date.
- `D+X`: the forward validation horizon after D.

Rules:

- production classification must use only data available on or before D
- forward D+X data must be loaded only after classification
- D+X validation must check whether the engine's classified setup was followed by actual price movement
- forward validation must report pass/fail/insufficient-data rather than silently assuming success
- D+X horizons should be configurable, with practical defaults such as D+1, D+2, D+5, D+10, and D+20 where supported by data

Self-backtesting is a quality gate for the signal engine. It is not permission to add unrelated strategies.

## Output And Audit Contract

Every result must be explainable.

Minimum required output fields:

- input symbol
- resolved provider symbol
- selected user path
- D-date
- final candidate class
- acceptance/rejection status
- reason codes
- L1 baseline state
- L2 routed path
- L3 evidence used
- D+X validation result where applicable
- provider/data status

The output should preserve V2-compatible visibility where useful, including reason-code discipline and CSV-friendly diagnostics.

## Explicit Non-Goals

The following are not part of the core V3 intent:

- default pan-USA market scanning
- default sector-by-sector calibration
- market regime modeling as a prerequisite for signal classification
- ETF portfolio mapping
- automated trading
- order execution
- position sizing
- portfolio allocation
- hidden strategy expansion beyond the three allowed paths
- changing path rules based on one isolated validation slice
- broad token-expensive recalibration unless explicitly approved by the user

These may be separate future projects or optional features only if the user explicitly requests them.

## Regression Risks To Eliminate

The central V3 risk is logical regression from mixed path behavior.

Known failure pattern:

- MACD is above the zero line
- stock is already in bullish continuation
- engine incorrectly labels it as `PRE_BULL_CROSSOVER`

V3 must prevent this class of error through L1 baseline facts, L2 path routing, path-specific L3 evidence, and rejection rules in L4.

Other risks:

- divergence being inferred from momentum rules
- crossover being used as a fallback when momentum logic fails
- D+X validation using future data during initial classification
- provider gaps being mistaken for signal weakness
- UI allowing selections that the engine cannot process consistently

## Referenced V2 Analysis Artifacts

The V2 analysis work and design artifacts are not absent; they are scattered. Future sessions should read these as supporting references, not as replacements for this canonical document.

Primary references:

- `docs/archive_unified_stock_scanner_engine_design.md`
- `docs/archive_unified_engine_recap_and_action_plan_2026-05-24.md`
- `docs/archive_technical_signal_processing_engine.md`
- `docs/analysis/current_engine_gap_analysis_against_fresh_charter_2026-06-01.md`
- `docs/analysis/v3_initial_engine_analysis_and_way_forward_2026-06-01.md`
- `docs/architecture/v2_operational_parity_contract.md`
- `validation/baselines/v3_baseline_acceptance_pack.md`

Key V2 model references:

- `docs/archive_unified_stock_scanner_engine_design.md`: path-first L1/L2/L3 model and baseline/router/evidence separation
- `docs/archive_unified_engine_recap_and_action_plan_2026-05-24.md`: V2 recap, L1/L2/L3 implementation action plan, and audit expectations
- `docs/architecture/v2_operational_parity_contract.md`: V2-style output visibility and operational parity expectations

## Development Rules For Future Sessions

Every future session must follow these rules:

1. Read this document first.
2. Check local and remote git state before editing.
3. State the exact code or documentation step before making changes.
4. Keep work scoped to the CSV-driven V3 engine unless the user explicitly asks for a separate feature.
5. Update documentation at the end of each completed step.
6. Commit locally at the end of each completed step when changes are valid.
7. Push to GitHub at the end of each completed step when network/authentication permits.
8. Update `docs/handover/current_session_handover.md` with current status and next steps.
9. If a requested or inferred task conflicts with this document, stop and ask the user before proceeding.

## Current Drift To Treat Carefully

Recent repository history includes sector, regime, and broad calibration work. Those artifacts should not be treated as V3's core product direction.

Do not delete or revert that history without explicit user approval. Treat it as historical context only.

The forward direction is this canonical intent:

```text
User CSV + user-selected path + V2 path-first levels + D-date processing + D+X self-backtesting
```

## Forward Implementation Plan

### Phase 1: Intent Lock And Audit

- add this canonical document
- update README and handover pointers
- audit `web_app_v3.py` and `src/stock_screener_v3` against this document
- list logic that belongs to V3 core versus drift artifacts

### Phase 2: Input And UI Contract

- enforce CSV upload/input as the primary universe source
- expose only the three allowed analysis options
- expose D-date and D+X controls
- prevent unsupported combinations in the UI

### Phase 3: L0/L1/L2/L3/L4/L5 Engine Structure

- formalize L0 input/data/date preparation
- formalize L1 baseline object
- formalize L2 router object
- split L3 evidence by path
- centralize L4 classification/rejection rules
- centralize L5 output/audit/backtesting

### Phase 4: V2 Logic Preservation

- recover and map V2 Crossover rules
- recover and map V2 Divergence rules
- recover and map V2 Momentum Setup / Bull Extension rules
- write path-specific parity tests before changing behavior

### Phase 5: Self-Backtesting

- implement D+X validation for accepted candidates
- keep classification no-lookahead clean
- report validation outcome per symbol
- add tests for D-date slicing and D+X horizons

### Phase 6: Web App Integration

- wire UI inputs to the engine contract
- keep output CSV/audit visible
- show provider/data failures cleanly
- preserve V2-style user diagnostics where useful

## Handover Instruction

For a new session:

1. Read this file.
2. Run:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -8
```

3. Read `docs/handover/current_session_handover.md`.
4. Continue only on tasks that align with this document unless the user explicitly changes direction.

