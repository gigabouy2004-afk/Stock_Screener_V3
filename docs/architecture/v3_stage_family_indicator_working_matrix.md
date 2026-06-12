# V3 Stage-Family Indicator Working Matrix

Last updated: 2026-06-13

Purpose: working table for constructing the V3 engine from V2 design intents without re-discovery. This is the editable matrix where indicators, gates, evidence modules, inputs, outputs, and path-specific meanings can be added, removed, or modified before coding.

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
- what outputs it should produce;
- what it must not override.

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

| Evidence / Indicator | API data required | V3 level | Crossover | Divergence | Momentum Setup / Bull Extension | Primary outputs | Guardrail |
|---|---|---:|---|---|---|---|---|
| User CSV symbol | CSV row | L0 | R | R | R | `Symbol`, `YahooSymbol`, source metadata | Supplied CSV is the universe; no hidden expansion. |
| User selected path | UI/input config | L0/L2 | R | R | R | `StageFamily`, selected family list | Only selected paths can produce final candidates. |
| D-date | UI/input config | L0/L5 | C/V | C/V | C/V | `DDate`, data cutoff | D+X data must not enter classification. |
| Close series | API historical price | L1/L3 | R/T | R/C | R/Q | close-derived indicators | Fetch through API per calculation; not a CSV requirement. |
| MACD 1D line/signal | Close series | L3/L4 | R/T for transition | C, swing support | Q/C for existing bull phase | `MACD_1D_Value`, `MACD_1D_Signal`, `MACD_1D_State` | Meaning differs by path; no global MACD rule. |
| MACD 1D crossover state | Close series | L3/L4 | R for bull/bear transition | C/A | C for bull phase already above signal | `MACD_1D_CrossoverState` | Above-zero bull continuation belongs to Momentum, not `PRE_BULL_CROSSOVER`. |
| MACD 1D crossover distance | Close series | L3/L4 | T for near transition | C/A | A/C | `MACD_1D_CrossoverDistance` | Nearness cannot override path boundary. |
| MACD 1D histogram | Close series | L3/L4 | T/Q, real/non-flat cross | R when compared to price swing | Q for expansion/continuation | `MACD_1D_Histogram`, `MACD_1D_PreviousHistogram` | No universal `histogram > 0.5` gate. |
| MACD histogram improving/deteriorating | Close series | L3/L4 | T for near bull/bear transition | R/C for confirmation turn | Q for improving momentum | `MACDHistogramImproving`, reason codes | Cannot promote developing divergence as confirmed without path rules. |
| MACD 4H state/crossover | API lower timeframe when requested | L3/L4 | T/Q confirmation only | N by default | N/TBD | `MACD_4H_State`, `MACD_4H_CrossoverState` | Fetch only when Crossover path requests lower-timeframe confirmation. |
| MACD 1H state/crossover | API lower timeframe when requested | L3/L4 | T/Q confirmation only | N by default | N/TBD | `MACD_1H_State`, `MACD_1H_CrossoverState` | Must not override 1D route. |
| Bars since MACD/signal cross | Close series | L3/L4/L5 | T freshness/staleness | A/C | A/C | `MACD_4H_BullCrossBarsAgo`, `MACD_1H_BullCrossBarsAgo`, related fields | Stale crosses remain auditable, not silently hidden. |
| Bars since zero-line cross | Close series | L3/L4/L5 | C/T | C/A | C/A | TBD output fields | Zero-line context is separate from crossover detection. |
| Historical MACD phase episodes | Close series, V2-style lookback | L3/L4 | S/C for crossover probability/readiness | C/A | R/Q for stock-specific momentum phase | `Momentum_Phase`, `Momentum_Strength`, maturity outputs TBD | Use inside selected path only; not a global route engine. |
| Momentum MACD baseline `8,21,5` | Close series | L3/L4 | N/C | N/C | R/Q | baseline MACD fields | Applies to Momentum methodology only unless user changes matrix. |
| RSI 1D | Close series | L3/L4 | Q/C recovery/weakening | R/Q for momentum disagreement | Q/S headroom | `RSI_1D`, `RSIScore` | RSI is not a global hard gate. |
| RSI upper boundary 80 | RSI 1D | L4 | N/C | C | S/Q | `RSIHeadroomTo80`, `RSIScore` TBD | Momentum scoring aid only: distance from current RSI to 80 can improve/reduce confidence, not route. |
| ADX 1D | API price series as required | L3/L4 | Q/C expansion support | C | Q/S trend confidence | `ADX_1D`, `ADX_State`, `ADXScore` | Low ADX should not automatically suppress early valid setups. |
| PlusDI / MinusDI | API price series as required | L3/L4 | Q buyer/seller participation | C | Q participation | `PlusDI_1D`, `MinusDI_1D` TBD | Directional participation only after path route is known. |
| EMA20 | Close series | L3/L4 | T/Q reclaim or loss | C | R/Q for re-entry/continuation | `EMA20`, `EMA20_Above`, `EMA20_Below` | EMA20 meaning is path-specific. |
| EMA20 reclaim | Close series | L3/L4 | T for bull transition | C | R for pullback re-entry | `EMA20_Reclaim` | Must not relabel continuation as crossover. |
| EMA20 rejection | Close series | L3/L4 | C/risk | Q/T for bear transition | C/risk | `EMA20_Rejection` | Use as context unless path defines it as route. |
| EMA50 | Close series | L3/L4 | Q/C trend stack | C | Q/S trend stack | `EMA50` TBD | Not a universal gate. |
| EMA200 | Close series | L3/L4 | C/risk/headroom | C support/resistance | Q/C risk/headroom | `EMA200`, `BelowEMA200` | Stage-specific evidence, not globally true gate. |
| Distance to EMA200 percent | Close series | L3/L4 | C/S | C/S | Q/S | `DistanceToEMA200Pct` | Can affect score/risk only after route. |
| EMA200 slope | Close series | L3/L4 | C/S | C/S | Q/S | `EMA200SlopeState` | Slope cannot create a candidate by itself. |
| Lifetime high | API long-range/lifetime history when requested | L3/L4 | C/S, not base route | C support/resistance | Q/S headroom/extension | `LifetimeHigh` | Request only when boundary analysis is selected/needed. |
| Distance to lifetime high percent | API long-range/lifetime history when requested | L4 | C/S | C/S | Q/S | `DistanceToLifetimeHighPct` | Bottom-level confidence aid only. |
| Lifetime high break count | API long-range/lifetime history when requested | L4/L5 | A/C | A/C | Q/S/A | `LifetimeHighBreakCount` | Does not override route. |
| EMA52 high / distance | API history where supported | L4 | C/S | C/S | Q/S | `EMA52High`, `DistanceToEMA52HighPct` | Confirm definition before coding. |
| EMA200 high / distance | API history where supported | L4 | C/S | C/S | Q/S | `EMA200High`, `DistanceToEMA200HighPct` | Confirm exact V2 meaning before coding. |
| One-month candle behavior | API monthly candles when requested | L3/L4 | C/Q | C/Q | Q/S | TBD monthly candle fields | Bounded context only; no broad scan. |
| Daily candle close location | API OHLC only when requested/available | L3/L4 | Q acceptance | C/Q | Q acceptance | `DailyCloseLocationPct` | Not required for MACD baseline. |
| Daily range vs 20-day average | API OHLC only when requested/available | L3/L4 | C/Q volatility | C/Q | C/Q | `DailyRangeVs20Avg` | Quality/context only. |
| Higher low 5D | API lows only when requested/available | L3/L4 | Q structure | R/Q for bullish geometry | R/Q pullback support | `HigherLow_5D` | Geometry meaning differs by path. |
| Lower high 5D | API highs only when requested/available | L3/L4 | C/risk | R/Q for bearish geometry | C/risk | `LowerHigh_5D` | Do not use as universal bearish override. |
| Range breakout up 20D | API highs/closes | L3/L4 | Q/C | C | Q continuation | `RangeBreakoutUp_20D` | Quality/context unless path says route. |
| Range breakdown down 20D | API lows/closes | L3/L4 | C/risk | C/Q bearish | C/risk | `RangeBreakdownDown_20D` | Do not suppress raw divergence silently. |
| Distance to 20D high | API highs/closes | L3/L4 | C/S | C/S | Q/S headroom | `DistanceTo20DHighPct` | Score aid only unless path contract changes. |
| Distance to 60D high | API highs/closes | L3/L4 | C/S | C/S | Q/S headroom | `DistanceTo60DHighPct` | Score aid only. |
| Bollinger percent-b | API Close | L3/L4 | Q/C recovery/compression | C/Q confirmation | C/Q extension risk | `Bollinger_PctB`, `Bollinger_Position` | No global Bollinger gate. |
| Bollinger bandwidth | API Close | L3/L4 | C/Q compression | C/Q | C/Q | `Bollinger_BandwidthPct` | Context only unless later scoped. |
| Volume latest | API volume when requested/available | L3/L4 | Q/C participation | C/Q | Q/C participation | `VolumeLatest` | Optional confirmation, not MACD baseline input. |
| Volume 20 average | API volume when requested/available | L3/L4 | Q/C | C/Q | Q/C | `Volume20Avg` | Missing volume should be auditable, not silently fatal. |
| Relative volume / intraday volume vs 20 avg | API volume when requested/available | L3/L4 | Q participation | C/Q | Q participation | `IntradayVolumeVs20Avg` | Not a base path selector. |
| Average daily volume metadata | CSV metadata/API profile cache | L0/L4 | C liquidity | C liquidity | C liquidity | `AvgDailyVolume` | Metadata/context; do not require live profile calls in hot path. |
| Average monthly volume metadata | CSV metadata/API profile cache | L0/L4 | C liquidity | C liquidity | C liquidity | `AvgMonthlyVolume` | Preserve if supplied. |
| Low liquidity tag | volume/profile metadata | L4/L5 | C risk | C risk | C risk | `LowLiquidity`, risk tags | Risk/review priority, not hidden rejection unless scoped. |
| PriceBand module | API price series | L3/L4 | TBD | TBD | TBD | TBD | V2 listed module; define row/cell before use. |
| StopLoss module | API price series | L3/L4/L5 | TBD | TBD | TBD | TBD | Not automated trading; if used, review/risk aid only. |
| Market regime | API benchmark data when requested/configured | L3/L4 | C | C | C | `MarketRegime` | Bounded context only; no universe expansion. |
| Sector context/regime | CSV sector + API benchmark only when requested/configured | L3/L4 | C | C | C | `SectorRegime` | Sector context for supplied CSV only; no sector calibration project. |
| Sector relative strength | API benchmark and symbol data | L3/L4 | TBD/C | TBD/C | Q/C when requested | TBD | Future bounded evidence, not broad scan. |
| AI / sentiment (`GetAI`) | External API/future provider | L3/L4 | TBD/C | TBD/C | TBD/C | TBD | Future optional evidence only after core engine is stable. |
| D+X endpoint return | API forward prices after classification | L5 | V | V | V | `DPlus{N}ReturnPct` | Validation only; no lookahead into classification. |
| D+X worst low return | API forward lows after classification | L5 | V | V | V | `DPlus{N}WorstLowReturnPct` | Validation only. |
| D+X best high return | API forward highs after classification | L5 | V | V | V | `DPlus{N}BestHighReturnPct` | Validation only. |
| Reason codes | evaluator output | L4/L5 | A | A | A | `ReasonCodes`, path reason fields | No failed check disappears silently. |
| WeightedScore | L4 scoring components | L4/L5 | S after Crossover route | S after Divergence route | S after Momentum route | `WeightedScore`, component scores | Never a global promotion gate or route selector. |

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

