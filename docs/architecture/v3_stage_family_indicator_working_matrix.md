# V3 Stage-Family Indicator Working Matrix

Last updated: 2026-06-13

Purpose: working table for constructing the V3 engine from V2 design intents without re-discovery. This is the editable matrix where indicator families, gates, evidence modules, inputs, outputs, and path-specific processing functions can be added, removed, or modified before coding.

Canonical scope: `docs/charter/v3_original_intent_and_handover.md`

Reference matrix: `docs/architecture/v3_evidence_stage_matrix.md`

V2 sources:

- `docs/archive_unified_stock_scanner_engine_design.md`
- `docs/archive_unified_engine_recap_and_action_plan_2026-05-24.md`
- `docs/architecture/v2_operational_parity_contract.md`

## Usage Rule

No indicator or evidence item should be implemented directly in an evaluator unless its row exists here or in the reference evidence-stage matrix.

Each row must answer:

- what API data is required;
- which V3 level owns the calculation;
- whether the item is route, timing, quality, context, scoring, audit, or validation;
- which path can use it;
- what exact processing function or condition set it should produce inside each stage-family cell;
- what it must not override.

## Matrix Representation Rule

Rows must be written as indicator families or evidence families, not as vague single values.

Examples:

- good row name: `MACD`
- weak row name: `MACD(1D)`

The cell under each stage family must contain the exact path-specific condition logic or processing function for that indicator family.

Examples:

- `CROSSOVER`: `MACD(1D) < Signal(1D)` and `Histogram(1D)` near zero, with optional same-analysis-point 4H/1H confirmation if requested.
- `DIVERGENCE`: price swing versus histogram swing disagreement plus confirmation turn.
- `SETUP`: `MACD(1D) > Signal(1D)` and bull-phase continuation/re-entry logic using the Setup baseline where applicable.

All indicator processing remains API/provider-driven. The matrix should describe the data needed from the provider, not assume hardcoded/static inputs inside evaluator logic.

Legend:

- `R`: route-defining evidence.
- `T`: timing/freshness evidence.
- `Q`: quality/confidence evidence.
- `C`: context/risk/review-priority evidence.
- `S`: scoring component only.
- `A`: audit/output only.
- `V`: validation/backtest only.
- `N`: not used by default.
- `TBD`: needs user confirmation before implementation.

## Core Path Matrix

| Indicator Family / Evidence | API data required | V3 level | CROSSOVER | DIVERGENCE | SETUP | Backtesting / D+X | Primary outputs | Guardrail |
|---|---|---:|---|---|---|---|---|---|
| User CSV symbol | CSV row | L0 | R | R | R | Use same supplied CSV universe for historical run. | `Symbol`, `YahooSymbol`, source metadata | Supplied CSV is the universe; no hidden expansion. |
| User selected path | UI/input config | L0/L2 | R | R | R | Execute the same selected path on D-date data. | `StageFamily`, selected family list | Only selected paths can produce final candidates. |
| D-date | UI/input config | L0/L5 | C/V | C/V | C/V | Primary historical analysis date; API data sliced as of D. | `DDate`, data cutoff | D+X data must not enter classification. |
| D+X date / horizon | UI/input config | L5 | V | V | V | Forward validation date/horizon after D. | `ForwardDays`, `DPlus{N}*` fields | D+X is validation only, never route evidence. |
| YFinance/provider historical pull | API provider | L0/L5 | V | V | V | Pull enough past data for D-date calculation plus forward data through D+X. | provider status, data errors | Same provider contract as live mode; provider gaps are reported. |
| D-date close price | API historical price | L0/L5 | V | V | V | Baseline price for D+X price check. | `DDateClose` TBD | Must be price available on or before D. |
| D+X close price | API forward price | L5 | V | V | V | Simple forward close comparison versus D. | `DPlus{N}ReturnPct` | Forward price is loaded after classification. |
| D+X high/low path | API forward high/low when available | L5 | V | V | V | Optional best-high/worst-low validation. | `DPlus{N}WorstLowReturnPct`, `DPlus{N}BestHighReturnPct` | Path validation is separate from simple endpoint check. |
| Close series | API historical price | L1/L3 | R/T | R/C | R/Q | Use only rows <= D for indicator values. | close-derived indicators | Fetch through API per calculation; not a CSV requirement. |
| MACD | Close series for 1D baseline; lower-timeframe API data only when requested | L3/L4 | `MACD(1D) < Signal(1D)` with `Histogram(1D)` near zero for near-bull transition; `MACD(1D) > Signal(1D)` with bear-side inverse for near-bear transition; optional same-analysis-point `4H` and `1H` confirmation only when requested. | Price swing versus histogram swing disagreement; confirmation requires the expected histogram turn, not MACD alone. | `MACD(1D) > Signal(1D)` / bull-phase continuation or re-entry logic; Setup-specific MACD baseline and historical phase behavior may refine quality. | Recompute the same MACD condition stack as of D and validate against D+X movement. | `MACD_1D_*`, optional `MACD_4H_*`, `MACD_1H_*`, phase outputs | `MACD` is an indicator family row; path cells must hold exact relations, not vague labels. |
| MACD crossover distance / freshness | Close series; lower-timeframe API data only when requested | L3/L4/L5 | Distance and bars-since-cross decide near-transition readiness and freshness. | Audit/context only unless a specific divergence rule later uses freshness. | Audit/context only unless Setup maturity later uses it. | Compare fresh versus stale D conditions by D+X outcome. | `MACD_1D_CrossoverDistance`, bars-since-cross fields | Distance/freshness cannot override path boundary by itself. |
| MACD zero-line context | Close series | L3/L4/L5 | Zero-line side and nearness are context for transition quality; not the crossover itself. | Context only by default. | Context only by default. | Compare D zero-line context buckets with D+X outcome. | zero-line context outputs TBD | Zero-line context is separate from crossover detection. |
| Historical MACD phase episodes / Setup baseline | Close series, V2-style lookback | L3/L4 | Probability/readiness aid only if explicitly approved. | Context/audit only by default. | Stock-specific bull/bear phase episodes, `MACD(8,21,5)` baseline where approved, maturity and percentile/history logic. | Validate whether D phase maturity/strength predicted D+X move. | `Momentum_Phase`, `Momentum_Strength`, maturity outputs TBD | Use only inside SETUP unless another path explicitly signs it off. |
| RSI 1D | Close series | L3/L4 | Q/C recovery/weakening | R/Q for momentum disagreement | Q/S headroom | Store D RSI and compare outcome buckets by D+X. | `RSI_1D`, `RSIScore` | RSI is not a global hard gate. |
| RSI upper boundary 80 | RSI 1D | L4 | N/C | C | S/Q | Validate Momentum headroom buckets against D+X. | `RSIHeadroomTo80`, `RSIScore` TBD | Distance from current RSI to 80 can affect confidence, not route. |
| ADX 1D | API price series as required | L3/L4 | Q/C expansion support | C | Q/S trend confidence | Validate ADX bucket contribution by D+X. | `ADX_1D`, `ADX_State`, `ADXScore` | Low ADX should not automatically suppress early valid setups. |
| PlusDI / MinusDI | API price series as required | L3/L4 | Q buyer/seller participation | C | Q participation | Validate D directional participation against D+X. | `PlusDI_1D`, `MinusDI_1D` TBD | Directional participation only after path route is known. |
| EMA20 | Close series | L3/L4 | T/Q reclaim or loss | C | R/Q for re-entry/continuation | Validate D EMA20 relation against D+X. | `EMA20`, `EMA20_Above`, `EMA20_Below` | EMA20 meaning is path-specific. |
| EMA20 reclaim | Close series | L3/L4 | T for bull transition | C | R for pullback re-entry | Validate D reclaim setups by D+X. | `EMA20_Reclaim` | Must not relabel continuation as crossover. |
| EMA20 rejection | Close series | L3/L4 | C/risk | Q/T for bear transition | C/risk | Validate rejection rows by D+X. | `EMA20_Rejection` | Use as context unless path defines it as route. |
| EMA50 | Close series | L3/L4 | Q/C trend stack | C | Q/S trend stack | Validate trend-stack buckets by D+X. | `EMA50` TBD | Not a universal gate. |
| EMA200 | Close series | L3/L4 | C/risk/headroom | C support/resistance | Q/C risk/headroom | Validate above/below EMA200 rows by D+X. | `EMA200`, `BelowEMA200` | Stage-specific evidence, not globally true gate. |
| Distance to EMA200 percent | Close series | L3/L4 | C/S | C/S | Q/S | Validate distance buckets by D+X. | `DistanceToEMA200Pct` | Can affect score/risk only after route. |
| EMA200 slope | Close series | L3/L4 | C/S | C/S | Q/S | Validate slope buckets by D+X. | `EMA200SlopeState` | Slope cannot create a candidate by itself. |
| Lifetime high | API long-range/lifetime history when requested | L3/L4 | C/S, not base route | C support/resistance | Q/S headroom/extension | Validate D boundary location by D+X. | `LifetimeHigh` | Request only when boundary analysis is selected/needed. |
| Distance to lifetime high percent | API long-range/lifetime history when requested | L4 | C/S | C/S | Q/S | Validate headroom buckets by D+X. | `DistanceToLifetimeHighPct` | Bottom-level confidence aid only. |
| Lifetime high break count | API long-range/lifetime history when requested | L4/L5 | A/C | A/C | Q/S/A | Validate breakout history buckets by D+X. | `LifetimeHighBreakCount` | Does not override route. |
| EMA52 high / distance | API history where supported | L4 | C/S | C/S | Q/S | Validate only after exact definition confirmed. | `EMA52High`, `DistanceToEMA52HighPct` | Confirm definition before coding. |
| EMA200 high / distance | API history where supported | L4 | C/S | C/S | Q/S | Validate only after exact V2 meaning confirmed. | `EMA200High`, `DistanceToEMA200HighPct` | Confirm exact V2 meaning before coding. |
| One-month candle behavior | API monthly candles when requested | L3/L4 | C/Q | C/Q | Q/S | Validate D monthly context against D+X. | TBD monthly candle fields | Bounded context only; no broad scan. |
| Daily candle close location | API OHLC only when requested/available | L3/L4 | Q acceptance | C/Q | Q acceptance | Validate acceptance buckets by D+X. | `DailyCloseLocationPct` | Not required for MACD baseline. |
| Daily range vs 20-day average | API OHLC only when requested/available | L3/L4 | C/Q volatility | C/Q | C/Q | Validate volatility buckets by D+X. | `DailyRangeVs20Avg` | Quality/context only. |
| Higher low 5D | API lows only when requested/available | L3/L4 | Q structure | R/Q for bullish geometry | R/Q pullback support | Validate D structure by D+X. | `HigherLow_5D` | Geometry meaning differs by path. |
| Lower high 5D | API highs only when requested/available | L3/L4 | C/risk | R/Q for bearish geometry | C/risk | Validate D structure by D+X. | `LowerHigh_5D` | Do not use as universal bearish override. |
| Range breakout up 20D | API highs/closes | L3/L4 | Q/C | C | Q continuation | Validate breakout rows by D+X. | `RangeBreakoutUp_20D` | Quality/context unless path says route. |
| Range breakdown down 20D | API lows/closes | L3/L4 | C/risk | C/Q bearish | C/risk | Validate breakdown rows by D+X. | `RangeBreakdownDown_20D` | Do not suppress raw divergence silently. |
| Distance to 20D high | API highs/closes | L3/L4 | C/S | C/S | Q/S headroom | Validate headroom buckets by D+X. | `DistanceTo20DHighPct` | Score aid only unless path contract changes. |
| Distance to 60D high | API highs/closes | L3/L4 | C/S | C/S | Q/S headroom | Validate headroom buckets by D+X. | `DistanceTo60DHighPct` | Score aid only. |
| Bollinger percent-b | API Close | L3/L4 | Q/C recovery/compression | C/Q confirmation | C/Q extension risk | Validate Bollinger buckets by D+X. | `Bollinger_PctB`, `Bollinger_Position` | No global Bollinger gate. |
| Bollinger bandwidth | API Close | L3/L4 | C/Q compression | C/Q | C/Q | Validate compression/expansion buckets by D+X. | `Bollinger_BandwidthPct` | Context only unless later scoped. |
| Volume latest | API volume when requested/available | L3/L4 | Q/C participation | C/Q | Q/C participation | Validate D volume support by D+X. | `VolumeLatest` | Optional confirmation, not MACD baseline input. |
| Volume 20 average | API volume when requested/available | L3/L4 | Q/C | C/Q | Q/C | Validate relative volume support by D+X. | `Volume20Avg` | Missing volume should be auditable, not silently fatal. |
| Relative volume / intraday volume vs 20 avg | API volume when requested/available | L3/L4 | Q participation | C/Q | Q participation | Validate participation buckets by D+X. | `IntradayVolumeVs20Avg` | Not a base path selector. |
| Average daily volume metadata | CSV metadata/API profile cache | L0/L4 | C liquidity | C liquidity | C liquidity | Validate liquidity risk buckets by D+X when metadata is available. | `AvgDailyVolume` | Metadata/context; do not require live profile calls in hot path. |
| Average monthly volume metadata | CSV metadata/API profile cache | L0/L4 | C liquidity | C liquidity | C liquidity | Validate liquidity risk buckets by D+X when metadata is available. | `AvgMonthlyVolume` | Preserve if supplied. |
| Low liquidity tag | volume/profile metadata | L4/L5 | C risk | C risk | C risk | Validate low-liquidity rows by D+X separately. | `LowLiquidity`, risk tags | Risk/review priority, not hidden rejection unless scoped. |
| PriceBand module | API price series | L3/L4 | TBD | TBD | TBD | No backtest until row/cell meaning is defined. | TBD | V2 listed module; define row/cell before use. |
| StopLoss module | API price series | L3/L4/L5 | TBD | TBD | TBD | If used, validate as path-risk review only. | TBD | Not automated trading; if used, review/risk aid only. |
| Market regime | API benchmark data when requested/configured | L3/L4 | C | C | C | Validate as bounded context split, not base route. | `MarketRegime` | Bounded context only; no universe expansion. |
| Sector context/regime | CSV sector + API benchmark only when requested/configured | L3/L4 | C | C | C | Validate as bounded context split for supplied CSV only. | `SectorRegime` | No sector calibration project by default. |
| Sector relative strength | API benchmark and symbol data | L3/L4 | TBD/C | TBD/C | Q/C when requested | No backtest until exact formula is defined. | TBD | Future bounded evidence, not broad scan. |
| AI / sentiment (`GetAI`) | External API/future provider | L3/L4 | TBD/C | TBD/C | TBD/C | No backtest until provider, timestamp, and no-lookahead rules are defined. | TBD | Future optional evidence only after core engine is stable. |
| Reason codes | evaluator output | L4/L5 | A | A | A | Required to explain D classification before D+X validation. | `ReasonCodes`, path reason fields | No failed check disappears silently. |
| WeightedScore | L4 scoring components | L4/L5 | S after Crossover route | S after Divergence route | S after Momentum route | Validate score buckets against D+X outcome. | `WeightedScore`, component scores | Never a global promotion gate or route selector. |

## Backtesting Workflow

Backtesting is a fourth validation column in the matrix, not a fourth signal path.

Required flow:

```text
CSV symbols
-> user-selected path: CROSSOVER / DIVERGENCE / MOMENTUM_SETUP
-> user-supplied historical D-date
-> API/provider fetches historical data needed for the selected path
-> engine slices data as of D
-> engine runs the same path logic used for live analysis
-> engine records D classification, reason codes, score, and evidence
-> user-supplied D+X horizon/date is loaded after classification
-> simple D close versus D+X close price check validates direction
-> optional D+X best-high/worst-low path metrics are recorded
```

Backtesting inputs:

- CSV universe.
- selected path or paths.
- D-date in the past.
- D+X horizon or explicit D+X date.
- provider/API configuration, currently yfinance-style in the existing implementation.

Backtesting outputs:

- D-date classification result.
- D-date evidence and reason codes.
- D-date price used for validation baseline.
- D+X close price.
- D+X return percentage.
- optional D+X worst-low and best-high returns.
- pass/fail/insufficient-data outcome.

No-lookahead rule:

```text
D+X data must be unavailable to L1/L2/L3/L4.
D+X data belongs only to L5 validation.
```

## Immediate Review Items

These rows need user review before coding:

- RSI upper boundary 80 and exact scoring formula for Momentum headroom.
- Exact meaning of `EMA52High`, `EMA200High`, and EMA lifetime-high percentage.
- Whether one-month candle behavior is a default Momentum aid or only user-requested.
- Whether sector/market context is shown as a score component or only as audit/context.
- Whether 4H/1H MACD belongs only to Crossover initially.
- Whether `PriceBand`, `StopLoss`, and `GetAI` remain future placeholders.

## Update Discipline

When a row is changed:

1. Update this matrix first.
2. Update `docs/charter/v3_original_intent_and_handover.md` only if the top-level contract changes.
3. Add or update tests before implementing behavior.
4. Keep output fields auditable.
5. Commit and push documentation and code at the end of the step.
