# Stock Screener V3_Charter Consolidated Engine Design

Last updated: 2026-06-16

Repo: `D:\Tools\Stock_Screener_V3`

Branch: `V3_Charter`

## Document Role

This document is the standalone consolidated charter for `V3_Charter`.

It is intended to capture, in one place:

- the business purpose of the engine;
- the allowed stage families and their meanings;
- the engine workflow and hierarchy;
- the scope boundaries and non-goals;
- the scoring and output contract;
- the data-provider rules;
- the matrix design and the current approved matrix content;
- the implementation guardrails needed to prevent path leakage and regression.

This document is comprehensive by design. A future session should be able to restart from this file alone and understand what the engine is trying to do, how it is meant to behave, and what must not be changed casually.

The original seed charter remains:

```text
docs/charter/v3_original_intent_and_handover.md
```

This consolidated document does not replace the original historical seed. It restates and integrates the approved intent in a standalone form.

## Core Purpose

`V3_Charter` is a CSV-based, user-directed equity screening engine.

Its purpose is to evaluate a user-supplied list of tickers and identify only those names that qualify for the user-selected technical stage family or families, using V2 as a reference library for technical-analysis indicator calculations and tuned threshold logic.

The engine is not meant to be:

- a broad default market scanner;
- a portfolio-management engine;
- a stop-loss engine;
- an automated trading system;
- an execution engine;
- a sector-calibration research project by default;
- a macro/regime platform by default;
- a universal pan-market screener unless the user explicitly supplies that universe.

The engine exists to answer a focused question:

```text
From the user-supplied equity universe, which tickers currently qualify for the selected technical opportunity family, and why?
```

## Business Meaning Of The Stage Families

The engine has exactly three user-facing stage families:

- `CROSSOVER`
- `DIVERGENCE`
- `SETUP`

There is no user-facing fourth family.

### CROSSOVER

`CROSSOVER` contains two critical business directions:

- `PRE_BULL_CROSSOVER`
- `PRE_BEAR_CROSSOVER`

`PRE_BULL_CROSSOVER` means:

- enter early enough to maximize the natural bull phase of the stock.

`PRE_BEAR_CROSSOVER` means:

- detect weakening early enough to support capital preservation and avoid future notional loss on an existing long-held equity.

This does not imply stop-loss trading logic. It means the engine must identify technically weakening holdings early enough to support an informed capital-preservation decision.

So `CROSSOVER` is not just a technical crossing event. It is the engine's transition-detection family for:

- early bull-phase entry;
- early bear-phase capital-preservation review.

### DIVERGENCE

`DIVERGENCE` means:

- validate whether a credible investment opportunity may be developing through meaningful disagreement between price behavior and momentum behavior.

`DIVERGENCE` is independent from `CROSSOVER` and `SETUP`. It must not be inferred just because another family fails.

### SETUP

`SETUP` means:

- a pure-play market-based entry path where technical-analysis indicators provide confidence/support for entering a new position;
- the position may be more temporary than a Pre-Bull entry because the current bull phase may later peak and rotate toward bear-side pressure.

`SETUP` is therefore not the same as `PRE_BULL_CROSSOVER`.

It is for:

- continuation;
- pullback re-entry;
- recovery within an existing bull structure;
- extension behavior where entry is still technically justified, but not at the very beginning of the natural bull phase.

## Engine Scope

The engine must:

- take a user-supplied CSV universe as the working universe;
- support stage-family selection;
- support user-selected qualifying filters;
- fetch required market data through an API/provider layer;
- process each ticker through a path-first technical engine;
- produce only qualified candidates for the selected family/families;
- rank those candidates within their family-specific scoring model;
- log rejected names with exact failure reasons;
- support D-date and D+X validation using the same logical engine.

The engine must not:

- silently expand the universe;
- infer extra stage families not chosen by the user;
- flatten all families into one undifferentiated ranking pool;
- let context rows override route logic;
- let one family's logic leak into another family's classification.

## User Workflow

The intended workflow is:

1. User supplies a CSV file containing ticker rows.
2. User selects one or more stage families.
3. User applies qualifying filters.
4. Engine loads only the data required for the selected logic.
5. Engine classifies each ticker.
6. Engine shows only qualifying candidates.
7. Engine logs non-qualifiers with exact reasons.
8. Engine can replay the same logic historically on D-date data and validate on D+X.

### Filter Contract

Filters are first-class engine inputs, not UI decoration.

Examples include:

- market cap;
- average volume;
- exchange;
- sector;
- industry;
- other metadata-based qualifying constraints.

The filter system exists before candidate display. A ticker that does not satisfy the filter contract is not a candidate, even if its technical state would otherwise be interesting.

### Candidate Display Contract

The engine is a selector, not a universal status reporter.

That means:

- qualifying tickers are shown;
- non-qualifying tickers are not shown as candidates;
- non-qualifying tickers are still logged in the processing output with reasons and relevant values.

`STATUS_QUO` is therefore not intended as a primary user-facing candidate family.

## Single-Engine Construction Rule

`V3_Charter` must be one cohesive engine.

It must not devolve into:

- separate stitched scripts;
- isolated family implementations with different design rules;
- uncontrolled indicator add-ons;
- route overrides caused by convenience code.

Everything must fit the same hierarchical engine:

```text
CSV input
-> user-selected path
-> API data retrieval required by that path
-> L0 preparation
-> L1 baseline
-> L2 route
-> L3 path-specific evidence
-> L4 classification and scoring
-> L5 output and D+X validation
```

## V2 Relationship

V2 is not the product model.

V2 is the reference library for:

- technical-analysis indicator calculations;
- tuned thresholds and parameter practice;
- diagnostic/output visibility;
- known evidence concepts.

V2 must not be copied forward blindly as finished engine behavior.

Any V2 component may be reused only if it is placed correctly in:

- the selected stage family;
- the correct hierarchy level;
- the matrix-approved row/cell meaning.

Key rule:

```text
V2 additions can refine confidence, risk, explanation, or score only inside the selected path trajectory.
They must not become base-level drivers.
```

## Engine Hierarchy

### L0: Input, Data, And Date Preparation

L0 prepares the run.

Responsibilities:

- load the CSV;
- normalize symbols;
- validate required fields;
- resolve provider symbols;
- capture the selected stage families;
- capture the selected filters;
- capture D-date and D+X settings where applicable;
- fetch data through the configured provider;
- isolate per-symbol provider/data failures.

### L1: Baseline

L1 establishes neutral technical facts.

Responsibilities:

- current MACD state;
- current moving-average context;
- current structure context;
- current volume/liquidity context where needed;
- any neutral facts required for safe routing.

L1 is not final classification.

### L2: Route

L2 decides which family or families are legitimately eligible, based on:

- user-selected family restriction;
- baseline facts;
- hard path boundaries.

L2 is where path leakage must be prevented.

Examples of prohibited leakage:

- a continuation state classified as a fresh crossover;
- divergence inferred because crossover failed;
- setup logic used as fallback after crossover failure.

### L3: Evidence

L3 calculates path-specific evidence only after route context is known.

Responsibilities:

- indicator computation on demand;
- derived evidence values;
- path-specific condition logic;
- evidence packaging for L4.

L3 must not perform broad global interpretation before path selection.

### L4: Classification And Scoring

L4 converts routed evidence into:

- candidate class;
- confidence/priority;
- weighted score;
- reason codes;
- rejection decisions.

Scoring is post-qualification only.

### L5: Output, Audit, And Validation

L5 produces:

- candidate CSV output;
- logs and summaries;
- rejection diagnostics;
- D+X validation records;
- provider/data status;
- enough audit fields to explain every pass/fail decision.

## Data Provider Contract

The engine must be API-driven.

The current free default backend is Yahoo Finance through `yfinance`, but the logic must remain behind a swappable provider abstraction.

The provider contract is:

- fetch only the fields required by the selected family and requested evidence;
- preserve deterministic D-date slicing;
- support per-symbol failure isolation;
- support forward D+X validation retrieval;
- avoid changing engine semantics through provider-specific quirks.

The engine must not assume universal OHLCV input.

Examples:

- MACD baseline logic may require only Close series;
- OHLC fields are only requested when a chosen evidence row needs them;
- volume is only required when the selected logic uses volume participation rows.

## Output And Audit Contract

Every result must be explainable.

Minimum output expectations:

- input symbol;
- resolved provider symbol;
- selected stage family;
- D-date;
- qualification result;
- final candidate class;
- weighted score;
- reason codes;
- routed path;
- evidence used;
- rejection reason where applicable;
- provider/data status;
- D+X validation result where applicable.

The V2-style auditability standard remains in force:

- visible diagnostics;
- CSV-friendly structure;
- component-level explainability;
- no silent drops of failed logic.

## Scoring Contract

WeightedScore is:

- per ticker;
- computed only after qualification;
- family-specific in meaning;
- grouped by family in display.

This means:

- a `PRE_BULL_CROSSOVER` ticker can score `81`;
- a `SETUP` ticker can also score `81`;
- those two scores are not a universal shared ranking by default.

The scoring formula belongs to the selected family and its active matrix rows.

Score is not route.
Score is not filter qualification.
Score is not a substitute for classification.

## D-Date And D+X Validation

Historical replay is a mandatory correctness tool.

Definitions:

- `D` = analysis date
- `D+X` = forward validation horizon

Rules:

- classification uses only data available on or before D;
- D+X data must not influence initial classification;
- the same logical engine must run on historical D data;
- D+X validates what happened after the classified signal.

This supports:

- engine qualification;
- regression checking;
- matrix-change validation.

Backtesting is not a fourth strategy path. It is a validation layer.

## Non-Goals

The engine is not intended for:

- automated trading;
- order execution;
- stop-loss trading logic;
- portfolio allocation;
- position sizing;
- portfolio management;
- silent universe expansion;
- default pan-USA screening;
- default sector-by-sector research;
- macro/regime expansion beyond bounded context rows;
- ad hoc threshold changes from one isolated observation.

## Regression Risks To Eliminate

The main failure mode is path leakage.

Known example:

- MACD already bullish above zero;
- stock is in continuation;
- engine incorrectly labels it `PRE_BULL_CROSSOVER`.

Other critical risks:

- divergence inferred from another family's failure;
- setup classified from crossover-style transition rules;
- context rows silently becoming route logic;
- future D+X data contaminating D classification;
- provider gaps misread as technical weakness.

## Consolidated Matrix Rules

The engine is governed by a stage-family indicator matrix.

### Matrix Shape

```text
Rows    = indicator families or evidence families
Columns = CROSSOVER, DIVERGENCE, SETUP
Cells   = exact path-specific condition logic or processing function
```

### Matrix Writing Rule

Use indicator families as rows.

Good:

- `MACD`
- `RSI`
- `EMA20`

Weak:

- `MACD(1D)` as a standalone row name

Reason:

the real meaning usually depends on a relation or condition, not on one naked value.

### Matrix Legend

- `Route`: helps decide whether a ticker belongs in that family.
- `Timing`: helps determine freshness, readiness, or staleness.
- `Quality`: strengthens or weakens confidence after route is known.
- `Context`: adds interpretation or risk context without deciding route by itself.
- `Scoring`: contributes to `WeightedScore` only after qualification.
- `Audit`: exists for explanation and visibility.
- `Validation`: belongs to D / D+X backtesting only.
- `Not used by default`: not part of default logic for that family.
- `TBD`: requires explicit signoff before implementation.

### Matrix Path Note

- `CROSSOVER` includes both `PRE_BULL_CROSSOVER` and `PRE_BEAR_CROSSOVER`.
- `PRE_BULL_CROSSOVER` is for early bull-phase entry.
- `PRE_BEAR_CROSSOVER` is for capital-preservation review on long-held equities.
- `DIVERGENCE` validates whether an opportunity may be developing.
- `SETUP` is a more tactical pure-play market-based entry path supported by TA confidence.

## Consolidated Matrix

| Indicator Family / Evidence | API data required | V3 level | CROSSOVER | DIVERGENCE | SETUP | Backtesting / D+X | Primary outputs | Guardrail |
|---|---|---:|---|---|---|---|---|---|
| User CSV symbol | CSV row | L0 | Route input: supplied universe only. | Route input: supplied universe only. | Route input: supplied universe only. | Use same supplied CSV universe for historical run. | `Symbol`, `YahooSymbol`, source metadata | Supplied CSV is the universe; no hidden expansion. |
| User selected path | UI/input config | L0/L2 | Route input: only selected path can qualify candidates. | Route input: only selected path can qualify candidates. | Route input: only selected path can qualify candidates. | Execute the same selected path on D-date data. | `StageFamily`, selected family list | Only selected paths can produce final candidates. |
| D-date | UI/input config | L0/L5 | Context plus validation boundary for all D-date calculations. | Context plus validation boundary for all D-date calculations. | Context plus validation boundary for all D-date calculations. | Primary historical analysis date; API data sliced as of D. | `DDate`, data cutoff | D+X data must not enter classification. |
| D+X date / horizon | UI/input config | L5 | Validation only after D classification is complete. | Validation only after D classification is complete. | Validation only after D classification is complete. | Forward validation date/horizon after D. | `ForwardDays`, `DPlus{N}*` fields | D+X is validation only, never route evidence. |
| Provider historical pull | API provider | L0/L5 | Validation support for replaying the same provider-backed calculation stack. | Validation support for replaying the same provider-backed calculation stack. | Validation support for replaying the same provider-backed calculation stack. | Pull enough past data for D-date calculation plus forward data through D+X. | provider status, data errors | Same provider contract as live mode; provider gaps are reported. |
| D-date close price | API historical price | L0/L5 | Validation baseline price for D outcome. | Validation baseline price for D outcome. | Validation baseline price for D outcome. | Baseline price for D+X price check. | `DDateClose` | Must be price available on or before D. |
| D+X close price | API forward price | L5 | Validation-only forward close price. | Validation-only forward close price. | Validation-only forward close price. | Simple forward close comparison versus D. | `DPlus{N}ReturnPct` | Forward price is loaded after classification. |
| D+X high/low path | API forward high/low when available | L5 | Validation-only forward path extremes. | Validation-only forward path extremes. | Validation-only forward path extremes. | Optional best-high/worst-low validation. | `DPlus{N}WorstLowReturnPct`, `DPlus{N}BestHighReturnPct` | Path validation is separate from simple endpoint check. |
| Close series | API historical price | L1/L3 | Route and timing input for close-derived calculations. | Route and context input for close-derived calculations. | Route and quality input for close-derived calculations. | Use only rows <= D for indicator values. | close-derived indicators | Fetch through API per calculation; not a CSV requirement. |
| MACD | Close series for 1D baseline; lower-timeframe API data only when requested | L3/L4 | `MACD(1D) < Signal(1D)` with `Histogram(1D)` near zero for near-bull transition; `MACD(1D) > Signal(1D)` with bear-side inverse for near-bear transition; optional same-analysis-point `4H` and `1H` confirmation only when requested. | Price swing versus histogram swing disagreement; confirmation requires the expected histogram turn, not MACD alone. | `MACD(1D) > Signal(1D)` / bull-phase continuation or re-entry logic; Setup-specific MACD baseline and historical phase behavior may refine quality. | Recompute the same MACD condition stack as of D and validate against D+X movement. | `MACD_1D_*`, optional `MACD_4H_*`, `MACD_1H_*`, phase outputs | `MACD` is an indicator family row; path cells must hold exact relations, not vague labels. |
| MACD crossover distance / freshness | Close series; lower-timeframe API data only when requested | L3/L4/L5 | Distance and bars-since-cross decide near-transition readiness and freshness. | Audit/context only unless a specific divergence rule later uses freshness. | Audit/context only unless Setup maturity later uses it. | Compare fresh versus stale D conditions by D+X outcome. | `MACD_1D_CrossoverDistance`, bars-since-cross fields | Distance/freshness cannot override path boundary by itself. |
| MACD zero-line context | Close series | L3/L4/L5 | Zero-line side and nearness are context for transition quality; not the crossover itself. | Context only by default. | Context only by default. | Compare D zero-line context buckets with D+X outcome. | zero-line context outputs | Zero-line context is separate from crossover detection. |
| Historical MACD phase episodes / Setup baseline | Close series, V2-style lookback | L3/L4 | Probability/readiness aid only if explicitly approved. | Context/audit only by default. | Stock-specific bull/bear phase episodes, `MACD(8,21,5)` baseline where approved, maturity and percentile/history logic. | Validate whether D phase maturity/strength predicted D+X move. | `Momentum_Phase`, `Momentum_Strength`, maturity outputs | Use only inside SETUP unless another path explicitly signs it off. |
| RSI 1D | Close series | L3/L4 | Quality and context for recovery or weakening after crossover conditions are already known. | Route support plus quality for momentum disagreement. | Quality and scoring input for setup headroom. | Store D RSI and compare outcome buckets by D+X. | `RSI_1D`, `RSIScore` | RSI is not a global hard gate. |
| RSI upper boundary | RSI 1D | L4 | Not used by default; optional context only if specifically approved. | Context only by default. | Scoring and quality input for remaining headroom below the configured upper boundary. | Validate headroom buckets against D+X. | `RSIHeadroom`, `RSIScore` | Distance to the upper boundary can affect confidence, not route. |
| ADX 1D | API price series as required | L3/L4 | Quality and context for trend expansion support. | Context for whether divergence has enough trend strength to matter. | Quality and scoring input for setup trend confidence. | Validate ADX bucket contribution by D+X. | `ADX_1D`, `ADX_State`, `ADXScore` | Low ADX should not automatically suppress early valid setups. |
| PlusDI / MinusDI | API price series as required | L3/L4 | Quality input for buyer versus seller participation after crossover conditions are known. | Context for directional participation around divergence. | Quality input for participation strength during continuation or re-entry. | Validate D directional participation against D+X. | `PlusDI_1D`, `MinusDI_1D` | Directional participation only after path route is known. |
| EMA20 | Close series | L3/L4 | Timing and quality input for reclaim, hold, or loss around transition. | Context for short-structure support or resistance. | Route and quality input for pullback re-entry or continuation. | Validate D EMA20 relation against D+X. | `EMA20`, `EMA20_Above`, `EMA20_Below` | EMA20 meaning is path-specific. |
| EMA20 reclaim | Close series | L3/L4 | Timing input for a possible bull transition. | Context only by default. | Route input for pullback re-entry. | Validate D reclaim setups by D+X. | `EMA20_Reclaim` | Must not relabel continuation as crossover. |
| EMA20 rejection | Close series | L3/L4 | Context and risk flag around failed reclaim. | Quality and timing signal for bear-side weakening only if divergence logic uses it. | Context and risk flag for setup weakness. | Validate rejection rows by D+X. | `EMA20_Rejection` | Use as context unless path defines it as route. |
| EMA50 | Close series | L3/L4 | Quality and context for broader trend stack support. | Context only by default. | Quality and scoring input for broader trend stack support. | Validate trend-stack buckets by D+X. | `EMA50` | Not a universal gate. |
| EMA200 | Close series | L3/L4 | Context, risk, and headroom signal; not a route trigger. | Context for major support or resistance. | Quality and context input for risk, headroom, and long-trend support. | Validate above/below EMA200 rows by D+X. | `EMA200`, `BelowEMA200` | Stage-specific evidence, not globally true gate. |
| Distance to EMA200 percent | Close series | L3/L4 | Context and scoring aid for how stretched price is versus EMA200. | Context and scoring aid only. | Quality and scoring aid for extension or headroom versus EMA200. | Validate distance buckets by D+X. | `DistanceToEMA200Pct` | Can affect score/risk only after route. |
| EMA200 slope | Close series | L3/L4 | Context and scoring aid for long-trend direction. | Context and scoring aid only. | Quality and scoring aid for long-trend direction. | Validate slope buckets by D+X. | `EMA200SlopeState` | Slope cannot create a candidate by itself. |
| Lifetime high | API long-range/lifetime history when requested | L3/L4 | Context and scoring aid only; never a base route trigger. | Context for major boundary support or resistance. | Quality and scoring input for headroom and extension risk. | Validate D boundary location by D+X. | `LifetimeHigh` | Request only when boundary analysis is selected/needed. |
| Distance to lifetime high percent | API long-range/lifetime history when requested | L4 | Context and scoring aid only. | Context and scoring aid only. | Quality and scoring aid for remaining headroom. | Validate headroom buckets by D+X. | `DistanceToLifetimeHighPct` | Bottom-level confidence aid only. |
| Lifetime high break count | API long-range/lifetime history when requested | L4/L5 | Audit plus context on prior breakout behavior. | Audit plus context on prior breakout behavior. | Quality, scoring, and audit input on prior breakout behavior. | Validate breakout history buckets by D+X. | `LifetimeHighBreakCount` | Does not override route. |
| EMA52 high / distance | API history where supported | L4 | Context and scoring aid once the exact V2 meaning is confirmed. | Context and scoring aid once the exact V2 meaning is confirmed. | Quality and scoring aid once the exact V2 meaning is confirmed. | Validate only after exact definition confirmed. | `EMA52High`, `DistanceToEMA52HighPct` | Confirm definition before coding. |
| EMA200 high / distance | API history where supported | L4 | Context and scoring aid once the exact V2 meaning is confirmed. | Context and scoring aid once the exact V2 meaning is confirmed. | Quality and scoring aid once the exact V2 meaning is confirmed. | Validate only after exact V2 meaning confirmed. | `EMA200High`, `DistanceToEMA200HighPct` | Confirm exact V2 meaning before coding. |
| One-month candle behavior | API monthly candles when requested | L3/L4 | Context and quality input from the monthly candle when explicitly requested. | Context and quality input from the monthly candle when explicitly requested. | Quality and scoring input from the monthly candle when explicitly requested. | Validate D monthly context against D+X. | monthly candle fields | Bounded context only; no broad scan. |
| Daily candle close location | API OHLC only when requested/available | L3/L4 | Quality input for candle acceptance near the close. | Context and quality input for candle acceptance. | Quality input for candle acceptance. | Validate acceptance buckets by D+X. | `DailyCloseLocationPct` | Not required for MACD baseline. |
| Daily range vs 20-day average | API OHLC only when requested/available | L3/L4 | Context and quality input for volatility versus normal range. | Context and quality input for volatility versus normal range. | Context and quality input for volatility versus normal range. | Validate volatility buckets by D+X. | `DailyRangeVs20Avg` | Quality/context only. |
| Higher low 5D | API lows only when requested/available | L3/L4 | Quality input for supportive short structure. | Route support plus quality input for bullish geometry. | Route support plus quality input for pullback structure. | Validate D structure by D+X. | `HigherLow_5D` | Geometry meaning differs by path. |
| Lower high 5D | API highs only when requested/available | L3/L4 | Context and risk flag for weaker short structure. | Route support plus quality input for bearish geometry. | Context and risk flag for weaker short structure. | Validate D structure by D+X. | `LowerHigh_5D` | Do not use as universal bearish override. |
| Range breakout up 20D | API highs/closes | L3/L4 | Quality and context input for breakout strength. | Context only by default. | Quality input for continuation strength. | Validate breakout rows by D+X. | `RangeBreakoutUp_20D` | Quality/context unless path says route. |
| Range breakdown down 20D | API lows/closes | L3/L4 | Context and risk flag for breakdown pressure. | Context plus quality input for bearish follow-through. | Context and risk flag for weakness. | Validate breakdown rows by D+X. | `RangeBreakdownDown_20D` | Do not suppress raw divergence silently. |
| Distance to 20D high | API highs/closes | L3/L4 | Context and scoring aid for nearby short-term resistance. | Context and scoring aid only. | Quality and scoring aid for headroom to recent highs. | Validate headroom buckets by D+X. | `DistanceTo20DHighPct` | Score aid only unless path contract changes. |
| Distance to 60D high | API highs/closes | L3/L4 | Context and scoring aid for nearby medium-term resistance. | Context and scoring aid only. | Quality and scoring aid for headroom to recent highs. | Validate headroom buckets by D+X. | `DistanceTo60DHighPct` | Score aid only. |
| Bollinger percent-b | API Close | L3/L4 | Quality and context input for recovery, compression, or stretch. | Context and quality input for confirmation or exhaustion. | Context and quality input for extension risk. | Validate Bollinger buckets by D+X. | `Bollinger_PctB`, `Bollinger_Position` | No global Bollinger gate. |
| Bollinger bandwidth | API Close | L3/L4 | Context and quality input for compression or expansion. | Context and quality input for compression or expansion. | Context and quality input for compression or expansion. | Validate compression/expansion buckets by D+X. | `Bollinger_BandwidthPct` | Context only unless later scoped. |
| Volume latest | API volume when requested/available | L3/L4 | Quality and context input for participation on the signal candle. | Context and quality input for participation on the signal candle. | Quality and context input for participation on the signal candle. | Validate D volume support by D+X. | `VolumeLatest` | Optional confirmation, not MACD baseline input. |
| Volume 20 average | API volume when requested/available | L3/L4 | Quality and context input for normal participation baseline. | Context and quality input for normal participation baseline. | Quality and context input for normal participation baseline. | Validate relative volume support by D+X. | `Volume20Avg` | Missing volume should be auditable, not silently fatal. |
| Relative volume / intraday volume vs 20 avg | API volume when requested/available | L3/L4 | Quality input for above-normal participation. | Context and quality input for above-normal participation. | Quality input for above-normal participation. | Validate participation buckets by D+X. | `IntradayVolumeVs20Avg` | Not a base path selector. |
| CMF | API OHLCV when requested/available | L3/L4 | Quality and context input for accumulation or distribution during pre-bull or pre-bear transition review. | Context and quality input for whether divergence is supported by money-flow behavior. | Quality and scoring input for continuation participation and accumulation support. | Validate CMF buckets by D+X. | `CMF_20` | Money-flow support only; cannot define the route by itself. |
| OBV | API close and volume when requested/available | L3/L4 | Quality and context input for whether volume flow is confirming pre-bull or pre-bear crossover direction. | Context and quality input for whether volume flow confirms or weakens the divergence reading. | Quality and scoring input for continuation or re-entry participation strength. | Validate OBV state and slope buckets by D+X. | `OBV_Slope_5`, `OBV_State` | Volume-flow support only; not a standalone stage trigger. |
| Efficiency ratio | API close series | L3/L4 | Quality and timing input for whether the transition is clean versus noisy. | Context and quality input for whether the swing structure is efficient or choppy. | Quality and scoring input for trend cleanliness during setup continuation or re-entry. | Validate efficiency buckets by D+X. | `EfficiencyRatio_10`, `DirectionalEfficiencyRatio_10`, `EfficiencyRatio_14`, `DirectionalEfficiencyRatio_14` | Trend-efficiency evidence cannot replace route logic. |
| Relative strength / benchmark relative performance | API symbol history plus benchmark history when requested/configured | L3/L4 | Context and quality input for whether the ticker is outperforming or underperforming its benchmark during transition review. | Context and quality input for whether the divergence is happening with supportive or weak relative performance. | Quality and scoring input for whether the setup is backed by relative outperformance. | Validate relative-strength buckets by D+X. | `RelativeReturn20DPct`, `RelativeReturn60DPct`, `RelativeTrendState`, `BenchmarkSymbol`, `BenchmarkReturn20DPct`, `BenchmarkReturn60DPct`, `BenchmarkRelativeReturn20DPct`, `BenchmarkRelativeReturn60DPct`, `BenchmarkRelativeTrendState` | Relative strength is supporting evidence only unless a later matrix rule explicitly promotes it. |
| Down volume pressure | API OHLCV when requested/available | L3/L4 | Context and risk flag for whether selling pressure is still heavy during bull-transition review, or supportive during bear-transition review. | Context and risk flag for whether selling pressure is contradicting or supporting the divergence case. | Context and risk flag for whether setup continuation still faces distribution pressure. | Validate down-pressure buckets by D+X. | `DownVolumePressure` | Pressure tagging should influence review quality, not silently kill valid path logic. |
| Failed high / ceiling structure | API highs, closes, and boundary history when requested/available | L3/L4 | Context and risk input for overhead resistance that may weaken a pre-bull transition, or confirm a pre-bear rollover. | Context and quality input for whether price is repeatedly failing near resistance during divergence formation. | Context, quality, and scoring input for extension risk or ceiling pressure in setup candidates. | Validate ceiling and failed-high buckets by D+X. | `FailedHighCount20D`, `CeilingPattern` | Ceiling structure is boundary evidence, not a standalone route selector. |
| Average daily volume metadata | CSV metadata/API profile cache | L0/L4 | Context input for liquidity suitability. | Context input for liquidity suitability. | Context input for liquidity suitability. | Validate liquidity risk buckets by D+X when metadata is available. | `AvgDailyVolume` | Metadata/context; do not require live profile calls in hot path. |
| Average monthly volume metadata | CSV metadata/API profile cache | L0/L4 | Context input for liquidity suitability. | Context input for liquidity suitability. | Context input for liquidity suitability. | Validate liquidity risk buckets by D+X when metadata is available. | `AvgMonthlyVolume` | Preserve if supplied. |
| Low liquidity tag | volume/profile metadata | L4/L5 | Context and risk flag for low tradability. | Context and risk flag for low tradability. | Context and risk flag for low tradability. | Validate low-liquidity rows by D+X separately. | `LowLiquidity`, risk tags | Risk/review priority, not hidden rejection unless scoped. |
| PriceBand module | API price series | L3/L4 | TBD pending exact path-specific meaning. | TBD pending exact path-specific meaning. | TBD pending exact path-specific meaning. | No backtest until row/cell meaning is defined. | TBD | Define row/cell before use. |
| Market regime | API benchmark data when requested/configured | L3/L4 | Context only as bounded market background. | Context only as bounded market background. | Context only as bounded market background. | Validate as bounded context split, not base route. | `MarketRegime` | Bounded context only; no universe expansion. |
| Sector context/regime | CSV sector + API benchmark only when requested/configured | L3/L4 | Context only as bounded sector background. | Context only as bounded sector background. | Context only as bounded sector background. | Validate as bounded context split for supplied CSV only. | `SectorRegime` | No sector calibration project by default. |
| Sector relative strength | API benchmark and symbol data | L3/L4 | TBD, with context-only use if later approved. | TBD, with context-only use if later approved. | Quality and context input when explicitly requested and defined. | No backtest until exact formula is defined. | TBD | Future bounded evidence, not broad scan. |
| AI / sentiment (`GetAI`) | External API/future provider | L3/L4 | TBD future context row only after provider, timestamp, and no-lookahead rules are defined. | TBD future context row only after provider, timestamp, and no-lookahead rules are defined. | TBD future context row only after provider, timestamp, and no-lookahead rules are defined. | No backtest until provider, timestamp, and no-lookahead rules are defined. | TBD | Future optional evidence only after core engine is stable. |
| Reason codes | evaluator output | L4/L5 | Audit output for why the ticker passed or failed Crossover. | Audit output for why the ticker passed or failed Divergence. | Audit output for why the ticker passed or failed Setup. | Required to explain D classification before D+X validation. | `ReasonCodes`, path reason fields | No failed check disappears silently. |
| WeightedScore | L4 scoring components | L4/L5 | Scoring output after the ticker already qualifies for Crossover. | Scoring output after the ticker already qualifies for Divergence. | Scoring output after the ticker already qualifies for Setup. | Validate score buckets against D+X outcome. | `WeightedScore`, component scores | Never a global promotion gate or route selector. |

## Immediate Approved Direction

From the current approved design:

- `PRE_BULL_CROSSOVER` and `PRE_BEAR_CROSSOVER` are both critical.
- `PRE_BEAR_CROSSOVER` is for capital-preservation review, not stop-loss automation.
- `DIVERGENCE` is opportunity validation.
- `SETUP` is a more tactical pure-play market-based entry path.
- `StopLoss` is out of scope and intentionally excluded.
- `AI` may exist later only as a bounded matrix-owned evidence row.

## Current Outstanding Review Items

These are still open for signoff before hardcoding behavior:

- exact `RSI` upper-bound scoring rule;
- exact meaning of `EMA52High`, `EMA200High`, and related long-boundary datapoints;
- whether one-month candle behavior is default for `SETUP` or only user-requested;
- whether sector/market context contributes to score or remains audit/context only;
- whether `4H` and `1H` MACD stay Crossover-only initially;
- whether `PriceBand` remains a future placeholder or becomes a signed-off matrix row.

## Restart Instruction

For a new session, read this file first, then verify:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -8
```

Then read:

```text
docs/handover/current_session_handover.md
```

Continue only with work that aligns to this consolidated charter unless the user explicitly changes direction.
