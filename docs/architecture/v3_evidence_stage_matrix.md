# V3 Evidence To Stage Matrix

Date: 2026-06-02

Purpose: define how one stock moves through the V3 engine from neutral evidence into stage-family evaluation, without letting one family rules leak into another.

This document is the V3 equivalent of the V2 route/indicator matrix. It is grounded in:

- V2 `engine_route_indicator_hierarchy.md`.
- V2 `unified_stock_scanner_engine_design.md`.
- PMDE vNext L1/L2/L3 architecture guardrails.

## 1. Core Principle

V3 evaluates a stock holistically, but not monolithically.

The engine must follow this sequence:

```text
UniverseRecord
-> PriceDataBundle
-> EvidencePack
-> Stage route candidates
-> Stage-family evaluators
-> best StageEvaluation
-> score/rank/audit output
```

The same neutral evidence field can mean different things in different stages. For example, `EMA200` is:

- trend-quality evidence for `MOMENTUM_SETUP`;
- risk/headroom context for `PRE_BULL_CROSSOVER`;
- bearish-structure support for `PRE_BEAR_CROSSOVER`;
- support/resistance context for `DIVERGENCE`.

Therefore, evidence calculation must remain separate from stage classification.

## 2. Family Boundary

| Stage Family | Candidate States | Engine Purpose |
|---|---|---|
| `CROSSOVER` | `PRE_BULL_CROSSOVER`, `PRE_BEAR_CROSSOVER` | Phase transition: seller-to-buyer entry review or buyer-to-seller exit/preservation review. |
| `MOMENTUM_SETUP` | `BULL_PULLBACK_REENTRY`, `BULL_CONTINUATION_MOMENTUM` | Bull phase continuation or re-entry after bullish phase already exists. |
| `DIVERGENCE` | `BULLISH_DIVERGENCE`, `BEARISH_DIVERGENCE`, `HIDDEN_BULLISH_DIVERGENCE`, `HIDDEN_BEARISH_DIVERGENCE` | Price and momentum disagreement. V1 evaluator implemented; calibration pending. |
| `STATUS_QUO` | `STATUS_QUO` | No selected family has sufficient route evidence. |

`CROSSOVER` must not claim bull pullback re-entry or bull continuation. Those belong to `MOMENTUM_SETUP`.

## 3. Route Outcome Contract

Every selected family must produce one of these outcomes for a stock:

| Outcome | Meaning |
|---|---|
| `SELECTED` | Valid stage candidate with enough quality for current review. |
| `WATCH` | Valid or relevant stage evidence, but quality/context needs manual review. |
| `REJECTED` | Stage route exists but score/quality is currently weak. Still auditable. |
| `STATUS_QUO` | No route for that family. |

No failed check should disappear silently. It should become a reason code, risk tag, or diagnostic field.

## 4. Current V3 Evidence Pack

| Evidence Section | Current Fields | Role |
|---|---|---|
| `stock_baseline` | `LatestPrice`, `LatestOpen`, `LatestHigh`, `LatestLow`, `DailyCloseLocationPct`, `DailyRangeVs20Avg` | Price location and candle acceptance. |
| `momentum` | `RSI_1D`, `MACD_1D_State`, `MACD_1D_CrossoverState`, `MACD_1D_Value`, `MACD_1D_Signal`, `MACD_1D_Histogram`, `MACD_1D_PreviousHistogram`, `MACD_1D_CrossoverDistance`, `MACDHistogramImproving` | MACD phase, transition, and momentum direction. |
| `trend` | `EMA20`, `EMA50`, `EMA200`, `DistanceToEMA200Pct`, `EMA200SlopeState`, `ADX_1D`, `ADX_State`, `PlusDI_1D`, `MinusDI_1D` | Trend structure and directional participation. |
| `volatility` | `Bollinger_PctB`, `Bollinger_BandwidthPct`, `DistanceTo20DHighPct`, `DistanceTo60DHighPct` | Location, compression/extension, and headroom. |
| `volume` | `VolumeLatest`, `Volume20Avg`, `IntradayVolumeVs20Avg` | Participation confirmation. |
| `structure` | `EMA20_Above`, `EMA20_Below`, `EMA20_Reclaim`, `HigherLow_5D`, `LowerHigh_5D`, `RangeBreakoutUp_20D`, `RangeBreakdownDown_20D`, `PriceLadder_Passed` | Price-structure route and quality evidence. |
| `risk_context` | `LowLiquidity`, `BelowEMA200` | Risk tags and review priority context. |
| `market_context` | `MarketRegime` | Broad market regime from configured benchmark data. Relative strength is not implemented yet. |
| `sector_context` | `SectorRegime` | Sector regime from configured benchmark data. Relative strength is not implemented yet. |

## 5. Evidence Role Matrix

Legend:

- `Route`: stage-defining evidence.
- `Timing`: freshness/actionability evidence.
- `Quality`: score/rank evidence.
- `Context`: risk, confidence, or review-priority evidence.
- `Audit`: output-only diagnostic.

| Evidence | Pre-Bull Crossover | Pre-Bear Crossover | Momentum Setup | Divergence |
|---|---|---|---|---|
| `MACD_1D_CrossoverState` | Route: bull cross or near bull transition. | Route: bear cross or near bear transition. | Context: bull phase should already be above signal. | Context, not primary route. |
| `MACD_1D_Histogram` | Timing: improving from seller/neutral control. | Timing: deteriorating from buyer/neutral control. | Quality: positive and expanding supports continuation. | Route input when compared to price swing behavior. |
| `MACD_1D_CrossoverDistance` | Timing: near transition if below/near signal. | Timing: near transition if above/near signal. | Audit/context only. | Context only. |
| `RSI_1D` | Quality: recovery zone, not a hard gate. | Quality: rolling down/weakening zone, not a hard gate. | Quality/context: constructive but not overheated. | Route/quality input for momentum disagreement. |
| `EMA20` / price vs EMA20 | Timing/quality: reclaim supports bull transition. | Timing/quality: loss/rejection supports bear transition. | Route: above/reclaiming EMA20 supports re-entry. | Confirmation/context. |
| `EMA50` | Quality/context: trend stack support. | Quality/context: trend stack weakness. | Quality: EMA20 above EMA50 supports bull phase. | Context. |
| `EMA200` / `DistanceToEMA200Pct` | Context/risk: below EMA200 is risk, not automatic rejection. | Quality/context: below or weakening EMA200 can support exit review. | Quality/context: above EMA200 preferred for bull continuation. | Support/resistance context. |
| `EMA200SlopeState` | Context: flat/rising improves confidence. | Context: falling/weakening improves exit confidence. | Quality/context: rising preferred. | Context. |
| `PlusDI_1D` / `MinusDI_1D` | Quality: buyer participation if `PlusDI >= MinusDI`. | Quality: seller participation if `MinusDI >= PlusDI`. | Quality: buyer participation. | Confirmation. |
| `ADX_1D` | Quality/context: expansion helps; low ADX can still be coil. | Quality/context: expansion helps; low ADX can still be early. | Quality: trend confirmation. | Context. |
| `IntradayVolumeVs20Avg` | Quality: participation support. | Quality: exit pressure confirmation. | Quality: continuation/re-entry participation. | Confirmation. |
| `DailyCloseLocationPct` | Quality: strong close supports acceptance. | Quality: weak close supports exit pressure. | Quality: strong close supports bull continuation. | Confirmation. |
| `EMA20_Reclaim` | Timing support for bull transition. | Not supportive. | Route for pullback re-entry. | Bullish confirmation. |
| `EMA20_Below` | Risk/context. | Route/quality support for bear transition. | Risk. | Bearish confirmation. |
| `HigherLow_5D` | Quality: constructive structure. | Opposite/risk. | Route/quality support for pullback re-entry. | Bullish divergence geometry support. |
| `LowerHigh_5D` | Risk/context. | Quality: bearish structure. | Risk/context. | Bearish divergence geometry support. |
| `RangeBreakoutUp_20D` | Quality/context. | Opposite/risk. | Quality: continuation support. | Context. |
| `RangeBreakdownDown_20D` | Risk/context. | Quality: exit pressure. | Risk. | Context. |
| `Bollinger_PctB` / bandwidth | Quality/context: recovery or compression. | Quality/context: rejection or expansion. | Quality/context: extension risk. | Confirmation/context. |
| `LowLiquidity` | Risk tag / review priority. | Risk tag / review priority. | Risk tag / review priority. | Risk tag / review priority. |
| `market_context` | Context/ranking. | Context/ranking. | Context/ranking. | Context/ranking. |
| `sector_context` | Context/ranking. | Context/ranking. | Context/ranking. | Context/ranking. |

## 6. Crossover Matrix

### `PRE_BULL_CROSSOVER`

Purpose:

```text
New capital entry review when momentum is transitioning from seller/neutral pressure into buyer control.
```

Hard route evidence:

- Daily MACD bull cross, or near bull transition with improving histogram.
- Direction must be bullish.

Quality/context evidence:

- EMA20 reclaim.
- Higher low.
- Buyer participation through DMI.
- Volume support.
- Strong daily close location.
- EMA200 risk/headroom context.

Output:

- `CandidateState = PRE_BULL_CROSSOVER`.
- `CrossoverDirection = BULLISH`.
- `CrossoverOpportunityType = BULLISH_TRANSITION_CROSSOVER` or `BULLISH_NEAR_TRANSITION`.

### `PRE_BEAR_CROSSOVER`

Purpose:

```text
Existing capital exit / capital-preservation review when momentum is transitioning from buyer/neutral support into seller control.
```

Hard route evidence:

- Daily MACD bear cross, or near bear transition with deteriorating histogram plus bearish structure/participation.
- Direction must be bearish.

Quality/context evidence:

- EMA20 loss or bearish position.
- Lower high.
- Seller participation through DMI.
- Volume support.
- Weak daily close location.
- EMA200 weakness can support exit logic.

Output:

- `CandidateState = PRE_BEAR_CROSSOVER`.
- `CrossoverDirection = BEARISH`.
- `CrossoverOpportunityType = BEARISH_TRANSITION_CROSSOVER` or `BEARISH_NEAR_TRANSITION`.

## 7. Momentum Setup Matrix

Purpose:

```text
Bull-phase continuation or re-entry after bullish phase already exists.
```

Momentum Setup is not a classical Crossover transition. It should only run when selected by the user or by the default holistic family set.

### `BULL_PULLBACK_REENTRY`

Route evidence:

- Daily MACD already above signal.
- Price above or reclaiming EMA20.
- EMA20 reclaim or higher-low behavior.

Quality evidence:

- Price above EMA200.
- EMA20 above EMA50.
- Buyer DMI support.
- Volume support.
- Strong close location.

Output:

- `CandidateState = BULL_PULLBACK_REENTRY`.
- `MomentumSetupOpportunityType = BULLISH_PULLBACK_REENTRY`.

### `BULL_CONTINUATION_MOMENTUM`

Route evidence:

- Daily MACD already above signal.
- Price above EMA20.
- Price ladder / trend stack support.
- Buyer DMI support or positive expanding histogram.

Quality evidence:

- Positive histogram.
- Histogram improving.
- EMA20 above EMA50.
- Price above EMA200.
- Volume and close-location support.

Output:

- `CandidateState = BULL_CONTINUATION_MOMENTUM`.
- `MomentumSetupOpportunityType = BULLISH_CONTINUATION_MOMENTUM` or `BULLISH_MOMENTUM_EXPANSION`.

## 8. Divergence Matrix Contract

Divergence V1 is implemented in V3. Its contract is defined in:

```text
docs/architecture/v3_divergence_contract.md
```

Its evaluator must not reuse Crossover hard gates or Momentum Setup continuation gates.

### Bullish Divergence

Expected route evidence:

- Price makes lower low or weak retest.
- Momentum makes higher low or improves.
- MACD can remain below zero.
- EMA200 is context, not a hard route gate.

### Bearish Divergence

Expected route evidence:

- Price makes higher high or failed breakout.
- Momentum makes lower high or weakens.
- MACD can remain above zero.
- EMA200 is context, not a hard route gate.

### Hidden Bullish Divergence

Expected route evidence:

- Price makes a higher low.
- Momentum makes a lower low or deeper pullback.
- Structure suggests continuation or pullback absorption, not a fresh Crossover transition.

### Hidden Bearish Divergence

Expected route evidence:

- Price makes a lower high.
- Momentum makes a higher high or stronger bounce.
- Structure suggests failed recovery or bear continuation, not a Momentum Setup route.

## 9. Stage Router Plan

Current V3 implementation:

```text
StageFamilyEvaluator(stage_families)
-> build one EvidencePack
-> build BaselineDecision from market, sector, and stock regimes
-> positively eliminate incompatible stage paths
-> evaluate remaining selected families
-> return highest-ranked StageEvaluation
```

Target V3 router:

```text
build EvidencePack
-> derive baseline phase: BULL / BEAR / MIXED / INSUFFICIENT
-> derive route candidates per selected family
-> evaluate only relevant families
-> rank family outputs
-> output best state plus audit for family decision
```

The target router must preserve user stage-family selection. If the user selects only `CROSSOVER`, Momentum Setup and Divergence should not produce final candidate states.

## 10. Implementation Rules

- Do not calculate stage decisions inside evidence generation.
- Do not use Crossover gates inside Momentum Setup or Divergence.
- Do not use Momentum Setup gates to suppress valid Crossover transition warnings.
- Treat EMA200, RSI, ADX, volume, and candle acceptance as stage-specific evidence, not globally true gates.
- Preserve all reason codes and route diagnostics in the output CSV.
- If evidence is relevant but incomplete, prefer `WATCH` or `REJECTED` with reason codes over silent `STATUS_QUO`.

## 11. Current V3 Status Against Matrix

Implemented:

- Neutral daily evidence pack.
- `CROSSOVER` evaluator with `PRE_BULL_CROSSOVER` and `PRE_BEAR_CROSSOVER`.
- `MOMENTUM_SETUP` evaluator with `BULL_PULLBACK_REENTRY` and `BULL_CONTINUATION_MOMENTUM`.
- `DIVERGENCE` evaluator with regular and hidden bullish/bearish candidate states.
- Stage-family dispatcher for selected families.
- Benchmark-backed market and sector regime context.
- Baseline positive-elimination router.
- Explicit `StockTraversalPlan` between baseline routing and evaluator dispatch.
- CSV diagnostics for Crossover and Momentum Setup route outputs.
- CSV diagnostics for Divergence route outputs.

Not implemented:

- Market/sector relative-strength evidence.
- Lower-timeframe 4H/1H bridge and trigger evidence.
- Stock-specific historical momentum baseline.
- Formal ranking layer beyond best `StageEvaluation` selection.
- Historical calibration for Divergence thresholds and swing geometry.
