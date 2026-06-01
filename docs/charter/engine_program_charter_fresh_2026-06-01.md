# Stock Screener Engine Program Charter

Date: 2026-06-01

Status: Fresh approach paper, independent of current implementation.

Purpose: restate the engine's original intent and define a clean way forward without being biased by the current code, accumulated patches, or recent one-case fixes.

## 1. Executive Intent

The engine is a user-driven tactical technical-analysis scanner.

Its job is to help the user discover stocks worth reviewing now. It is not a fully automated trading system and should not behave like one.

The engine should answer:

```text
Given a user-selected universe and stage family, which stocks are technically interesting today, why, and with what quality of evidence?
```

It should not try to answer:

```text
How much capital should I deploy?
Where exactly is the stop-loss?
What is the exact buy price?
Should an order be placed automatically?
```

The engine should be optimized for:

- Candidate discovery.
- Clear stage classification.
- Explainable technical evidence.
- Practical scan speed.
- Honest separation between signal validity and follow-through probability.
- Continuous validation without overfitting to one failed example.

## 2. Operating Philosophy

The engine must remain path-first, not indicator-first.

The correct sequence is:

```text
Universe -> Market/Sector Context -> Stock Baseline -> Stage Route -> Evidence Pack -> Classification -> Score -> Rank -> Audit
```

The incorrect sequence is:

```text
Calculate every indicator -> add gates after failures -> keep tightening until one bad event disappears
```

The second pattern creates a restrictive, fragile engine. It can explain past failures but may stop finding future opportunities.

## 3. Program Scope

### In Scope

- User-provided universe scans.
- CSV and manual-symbol inputs.
- Exchange, sector, industry, liquidity, and price filters where metadata exists.
- Stage-family selection:
  - Crossover.
  - Divergence.
  - Momentum Trading.
- Technical baseline calculation.
- Market and sector context.
- Stage-specific evidence and scoring.
- Candidate ranking.
- Audit columns and reason codes.
- Historical replay and forward validation.

### Out Of Scope

- Automated order execution.
- Position sizing.
- Capital allocation.
- Portfolio risk management.
- Final trade management.
- Guaranteeing D+1 or D+2 profitability.
- Reclassifying every event-driven failure as a technical-rule failure.

## 4. Core Product Contract

For every scan, the engine should return three layers of truth.

### Layer 1: Classification

What state is the stock in?

Examples:

- `PRE_BULL_CROSSOVER`
- `PRE_BEAR_CROSSOVER`
- `BULLISH_DIVERGENCE`
- `BEARISH_DIVERGENCE`
- `MOMENTUM_SETUP`
- `STATUS_QUO`

Classification should describe technical state, not guaranteed profit.

### Layer 2: Quality

How good is the evidence?

Quality should be expressed as:

- Score.
- Confidence bucket.
- Key positive evidence.
- Key risks.

Quality is not a binary gate unless the missing evidence invalidates the stage definition itself.

### Layer 3: Context

What outside or surrounding conditions matter?

Examples:

- Broad market trend.
- Sector trend.
- Sector-relative strength.
- Earnings or major event proximity.
- Nearby resistance or overhead supply.
- Liquidity.
- Volatility.

Context should mostly affect ranking, confidence, and review priority. It should not silently erase a valid technical classification unless the program explicitly defines that context as disqualifying.

## 5. Stage-Family Definitions

### Crossover

Intent:

Identify stocks transitioning from one momentum phase to another before the move is fully obvious.

Pre-Bull Crossover should mean:

```text
The stock is showing credible early evidence of bullish transition.
```

It should not mean:

```text
The stock is guaranteed to rise in the next two sessions.
```

Required evidence:

- Daily momentum is in or near a transition zone.
- Lower timeframe confirms timing or early acceptance.
- Price is not structurally broken.
- The signal is recent enough to be actionable.

Quality evidence:

- Strong close location.
- Improving histogram or actual crossover.
- Price reclaim or higher-low behavior.
- Volume support.
- Improving relative strength.
- Enough headroom before resistance.

Risks:

- Choppy regime.
- Weak participation.
- Failed prior highs.
- Event risk.
- Overhead supply.
- Poor liquidity.

### Divergence

Intent:

Identify disagreement between price and momentum where reversal risk or opportunity is increasing.

Required evidence:

- Price makes a new high/low while momentum fails to confirm.
- Divergence is recent enough to matter.
- Direction and timeframe are explicit.

Quality evidence:

- Divergence at support/resistance.
- Volume confirmation.
- Reversal candle.
- Sector or market alignment.

### Momentum Trading

Intent:

Identify stocks already in constructive trend continuation or expansion.

Required evidence:

- Existing trend structure.
- Momentum remains active.
- Price is not excessively extended unless explicitly flagged.

Quality evidence:

- Relative strength.
- Volume expansion.
- Pullback-and-reclaim behavior.
- Trend persistence.

## 6. Hard Gates Versus Score Factors

The engine should distinguish invalidating evidence from quality evidence.

### Hard Gates

Hard gates should be rare. They define whether a candidate can belong to a stage at all.

Examples:

- Missing price data.
- Insufficient history.
- A selected Crossover route has no actual crossover-transition evidence.
- A bullish stage requested but the route only supports bearish evidence.
- User filter excludes the symbol.

### Score Factors

Score factors change confidence and ranking.

Examples:

- ADX level.
- Efficiency Ratio.
- CMF.
- OBV.
- Volume versus average.
- Candle close quality.
- Benchmark relative strength.
- Distance to resistance.
- Event risk.

The default design principle:

```text
If evidence changes probability but does not change the technical state, score it. Do not gate it.
```

## 7. Market And Sector Context

Market and sector context should exist before stock-level ranking.

Minimum context:

- Broad market direction:
  - SPY or QQQ for US stocks.
  - NIFTY 50 for NSE stocks.
- Sector benchmark direction:
  - Sector ETFs or locally maintained sector indices.
- Stock relative strength versus:
  - Market benchmark.
  - Sector benchmark.

Context output should include:

- MarketRegime.
- SectorRegime.
- RelativeStrength20D.
- RelativeStrength60D.
- RelativeTrendState.

Interpretation:

- A weak market does not mean no stock can be selected.
- A weak sector does not mean no stock can be selected.
- But weak context should reduce rank and confidence unless the stock is clearly outperforming.

## 8. Event Risk

The engine should separate technical signal validity from event-driven failure risk.

Event risk examples:

- Earnings within the last 5 trading days.
- Earnings within the next 5 trading days.
- Guidance change.
- Analyst downgrade or major target cut.
- Offering, dilution, regulatory, litigation, or management shock.

Event risk output should include:

- EventRiskFlag.
- EventRiskType.
- EventRiskDate.
- EventRiskAgeDays.

Interpretation:

```text
Valid technical signal + event risk = valid signal, lower confidence or review priority.
```

Event risk should not be retroactively treated as proof that the technical signal was invalid.

## 9. Scoring Model

Scores should be stage-specific.

Suggested top-level scoring buckets:

| Bucket | Purpose |
|---|---|
| Route Validity | Does the stock belong to the stage? |
| Timing | Is the signal fresh/actionable? |
| Price Structure | Is price behaving constructively? |
| Participation | Are volume/money-flow indicators supportive? |
| Market/Sector Context | Is the surrounding environment supportive? |
| Risk Context | Event risk, resistance, liquidity, volatility |

For Crossover, suggested weighting:

| Component | Weight |
|---|---:|
| Route/timing | 30 |
| Price structure | 20 |
| Participation | 15 |
| Candle/intraday acceptance | 15 |
| Market/sector relative strength | 10 |
| Risk/headroom context | 10 |

Scores should be calibrated by validation, not by intuition.

## 10. Output Classes

The engine should separate candidate class from review priority.

Candidate class:

- `SELECTED`
- `WATCH`
- `REJECTED`
- `STATUS_QUO`

User-facing state:

- `PRE_BULL_CROSSOVER`
- `PRE_BEAR_CROSSOVER`
- `BULLISH_DIVERGENCE`
- `BEARISH_DIVERGENCE`
- `MOMENTUM_SETUP`
- `STATUS_QUO`

Review priority:

- `A`
- `B`
- `C`
- `Event Risk`
- `Low Liquidity`
- `Needs Manual Review`

This prevents a valid technical signal from being hidden simply because it has context risk.

## 11. Validation Discipline

Validation must not be optimized around one failed ticker.

Every rule change should be tested across:

- Multiple D dates.
- Multiple sectors.
- Random samples.
- First-candidate scans.
- Ranked full-universe scans where runtime allows.
- D+1, D+2, and D+5 outcomes.

Validation should report:

- Symbols scanned.
- Candidates found.
- Candidate density.
- Pass rate among candidates.
- Average and median returns.
- Distribution of failures.
- Event-risk failures separately from technical failures.
- Whether candidates were first N found or top N ranked.

Minimum useful validation format:

```text
D date:
Universe:
Sector filter:
Symbols scanned:
Candidates selected:
Candidate density:
D+1 pass:
D+2 pass:
D+5 pass:
Failures:
Failure categories:
Rule changes tested:
Decision:
```

## 12. Historical Backtesting Engine

A dedicated historical backtesting engine is a core deliverable, not an optional helper script.

Purpose:

```text
Run the same production signal engine as if today were a chosen historical date, produce only the candidates that would have been visible on that date, and validate those candidates against future bars that were not available to the engine at decision time.
```

This is critical because manual live validation and one-off replays are not enough to prove whether the engine is useful.

### Backtesting Principles

The backtesting engine must follow these rules:

- No look-ahead bias.
- No future data in indicators, profile metadata, event flags, or rankings.
- Same stage engine as production, not a separate simplified backtest model.
- Same configuration defaults unless a test explicitly overrides them.
- Same user-selectable universe and filters.
- Same output columns as live execution, plus validation columns.
- Reproducible random sampling when random samples are used.
- Explicit distinction between first N candidates found and top N ranked candidates.

### Historical Execution Contract

For a given D date, the backtester must:

1. Load the chosen universe as it is intended to be tested.
2. Load only OHLCV data available up to D.
3. Load market and sector benchmark data only up to D.
4. Load metadata and event context as-of D where available.
5. Execute the same production engine.
6. Produce candidates valid as of D.
7. Load forward bars only after candidate generation is complete.
8. Measure D+1, D+2, D+5, and configurable forward outcomes.
9. Write summary and full detail artifacts.

### Required Inputs

- Universe file.
- D date.
- Stage family or families.
- Optional sector/exchange/industry filters.
- Candidate count target.
- Scan limit or full-universe mode.
- Forward validation horizons:
  - D+1.
  - D+2.
  - D+5.
  - Optional D+8 or D+10.
- Sampling mode:
  - Sequential first N.
  - Deterministic random N.
  - Full universe.
  - Sector-filtered.
- Random seed when random sampling is used.
- Engine configuration version.

### Required Outputs

The backtester must produce:

- Detail CSV.
- Summary markdown.
- Optional HTML report.
- Optional aggregate scorecard across multiple D dates.

Detail output should include:

- Symbol.
- CompanyName.
- Exchange.
- Sector.
- Industry.
- D date.
- D close.
- CandidateState.
- CandidateClass.
- ReviewPriority.
- WeightedScore.
- Confidence.
- All evidence-pack fields.
- All reason codes.
- MarketRegime as of D.
- SectorRegime as of D.
- EventRiskFlag as of D.
- Resistance/headroom fields as of D.
- D+1 close and return.
- D+2 close and return.
- D+5 close and return.
- Pass/fail by horizon.
- Failure category where classifiable.

Summary output should include:

- Universe size.
- Symbols successfully processed.
- Symbols skipped and skip reasons.
- Candidates found.
- Candidate density.
- Pass rate by horizon.
- Average return by horizon.
- Median return by horizon.
- Best and worst candidates.
- Pass rate by sector.
- Pass rate by score bucket.
- Pass rate by confidence bucket.
- Pass rate by review priority.
- Event-risk candidate performance.
- Top recurring reason codes among failures.

### Backtesting Modes

The backtester should support at least four modes.

#### Mode 1: Single-Date Replay

Run one D date and one universe.

Use this for debugging and manual review.

#### Mode 2: Multi-Date Replay

Run many D dates over the same universe.

Use this for robustness testing across market regimes.

#### Mode 3: Random-Lot Replay

Run deterministic random samples.

Use this to avoid only testing familiar symbols.

#### Mode 4: Full-Universe Ranked Replay

Run the full universe, rank candidates, and evaluate top N.

Use this for the closest approximation of real scanner behavior.

### Success Metrics

Backtesting should not only ask, "Did the selected stocks go up?"

It should measure:

- Candidate density.
- Candidate quality.
- Ranking quality.
- Signal freshness.
- Forward return distribution.
- Failure concentration by reason code.
- Whether score buckets separate outcomes.
- Whether the engine finds enough candidates to be useful.

Minimum program-level metrics:

| Metric | Meaning |
|---|---|
| Candidate Density | Selected candidates / symbols processed |
| D+1 Hit Rate | Percent positive by next session |
| D+2 Hit Rate | Percent positive by second session |
| D+5 Hit Rate | Percent positive by fifth session |
| Median D+2 Return | Typical short-term follow-through |
| Score Separation | Higher score buckets outperform lower score buckets |
| Failure Explainability | Failed candidates have auditable risk/context reasons |

### Acceptance Criteria

Before a scoring model is promoted, it should pass a defined validation pack.

Minimum validation pack:

- At least 5 D dates.
- At least 3 market environments where possible:
  - bullish.
  - bearish.
  - choppy.
- At least 3 sector-restricted tests.
- At least one random-lot test per D date.
- At least one full-universe or large-universe ranked test.
- Reported candidate density and hit rate.

Promotion should require:

- Candidate density high enough to be useful.
- Score buckets show some separation.
- Failures are not dominated by one unmodeled risk.
- The model improves versus the previous baseline on more than one D date.

### Anti-Bias Rules

The backtesting engine must prevent these common mistakes:

- Do not pick dates only after seeing known winners.
- Do not tune a rule on one ticker and claim improvement.
- Do not mix live current metadata into historical replay without marking it.
- Do not count skipped symbols as clean rejects.
- Do not hide candidate scarcity behind high pass rate.
- Do not report only successful candidates.
- Do not compare first-candidate runs against ranked full-universe runs as if they are equivalent.

### Role In Development Workflow

Every meaningful engine change should follow:

```text
Change hypothesis
-> implement in branch
-> compile
-> run standard backtest pack
-> compare against baseline
-> decide keep/refactor/revert
-> document result
```

The backtesting engine is therefore the quality gate for engine evolution.

## 13. Data Model Requirements

The engine needs a stable local universe baseline.

Required universe fields:

- Symbol.
- YahooSymbol.
- CompanyName.
- Exchange.
- Sector.
- Industry.
- InstrumentType.
- MarketCap.
- AvgDailyVolume.
- SourceFile.
- LastProfileRefreshDate.

Runtime scans should not depend on per-symbol profile calls for basic metadata.

Historical replay and backtesting must preserve the same metadata used for sample selection. If a test is sector-filtered, the output should retain the sector used for that test.

## 14. Proposed Clean Architecture

### Module 1: Universe Loader

Responsibilities:

- Load symbols and metadata.
- Normalize Yahoo symbols.
- Remove duplicates.
- Preserve source metadata.

### Module 2: Data Provider

Responsibilities:

- Fetch daily and intraday OHLCV.
- Fetch benchmark series.
- Cache per run.
- Record provider and timestamp.

### Module 3: Baseline Calculator

Responsibilities:

- Calculate only neutral baseline facts:
  - Trend.
  - Momentum.
  - Volatility.
  - Liquidity.
  - Market/sector context.

No final candidate decisions here.

### Module 4: Stage Router

Responsibilities:

- Determine which stage families should run.
- Route a stock to Crossover, Divergence, Momentum Trading, or no route.

### Module 5: Stage Evaluators

Responsibilities:

- Evaluate stage-specific hard requirements.
- Build evidence packs.
- Return selected/watch/rejected state with reason codes.

### Module 6: Scoring And Ranking

Responsibilities:

- Score selected and watch candidates.
- Apply context penalties.
- Rank candidates.

### Module 7: Audit And Output

Responsibilities:

- Produce user-facing results.
- Produce full diagnostic output.
- Preserve all reason codes.
- Make validation reproducible.

### Module 8: Backtesting And Validation

Responsibilities:

- Execute the production engine as of historical D dates.
- Prevent look-ahead bias.
- Preserve as-of metadata.
- Validate forward outcomes.
- Compare changes against baselines.
- Produce repeatable scorecards.

## 15. Lessons From The Current Engine

Useful lessons to keep:

- Directional Crossover routes are necessary.
- Reason codes are valuable.
- Fixed-date replay is essential.
- Lower-timeframe confirmation catches some weak timing.
- EMA200 reclaim context can be useful.
- Confirmation scoring improves explainability.
- Benchmark-relative diagnostics are useful but should not be hard gates by default.
- Candidate density must be measured, not assumed.

Problems to avoid:

- Turning every failure into a new hard gate.
- Mixing route eligibility and quality scoring.
- Letting one stage family's rules leak into another.
- Treating D+1/D+2 failure as automatic proof that classification was invalid.
- Running historical tests without preserved sector/metadata context.
- Using score labels that imply predictive certainty before validation supports them.

## 16. Current Engine Gap Map

This section maps the fresh charter against the current implementation at a high level.

### Aligned

- The engine has user-driven universe scanning.
- It supports stage families.
- It has Crossover, Divergence, and Momentum paths.
- It has reason codes and audit columns.
- It has fixed-date replay support.
- It can validate D+1/D+2 outcomes.
- It has started adding confirmation and benchmark-relative diagnostics.
- It has an early fixed-date replay script that proves the concept of historical execution.

### Partially Aligned

- Path-first routing exists, but the current Crossover path has accumulated many tactical patches.
- Scoring exists, but score components are not yet calibrated enough to rank winners reliably.
- Market/sector context exists only partially and is not backed by durable local sector metadata in historical replay.
- Watch/internal states exist, but output policy is still evolving.
- Validation exists, but candidate-density reporting is still manual.
- Historical replay exists, but it is not yet a complete first-class backtesting engine with preserved metadata, multi-date scorecards, and standard acceptance packs.

### Not Aligned

- Basic metadata is not consistently preserved through historical replay.
- Event risk is not modeled.
- Resistance/headroom is still too shallow for practical decision quality.
- The engine still uses several binary blocks that should probably be score/context factors.
- There is no clean separation between technical signal validity and follow-through risk.
- The current scoring branch is not proven enough to merge as the new model.
- There is no formal backtesting quality gate for every engine change.

## 17. Recommended Way Forward

### Phase 1: Freeze Current Experimental Tuning

Stop adding hard gates to the current Crossover path.

Keep the current branch as an evidence branch, not a final model.

### Phase 2: Build A Clean Metadata Baseline

Create enriched universe files for US and NSE symbols.

This is foundational. Without stable sector/industry/event metadata, market/sector validation remains unreliable.

### Phase 3: Build The Backtesting Engine

Promote historical replay into a proper backtesting subsystem.

Required first version:

- Single-date replay.
- Random-lot replay.
- Sector-filtered replay.
- D+1, D+2, D+5 validation.
- Candidate density reporting.
- Baseline comparison output.
- Preserved universe metadata.

No major signal redesign should be accepted without this validation layer.

### Phase 4: Implement A Clean Evidence Pack

For each stage candidate, output:

- Route evidence.
- Timing evidence.
- Price-structure evidence.
- Participation evidence.
- Market/sector context.
- Risk/headroom context.
- Event-risk context.

Do this before changing more thresholds.

### Phase 5: Rebuild Crossover Evaluation Around Evidence Classes

Crossover should produce:

- Valid technical route.
- Timing state.
- Quality score.
- Context risk.
- Review priority.

Avoid using every weak quality point as a hard rejection.

### Phase 6: Validate Before Optimizing

Run repeatable tests:

- Full universe or large random samples.
- Sector-specific samples.
- Multiple D dates.
- D+1, D+2, D+5.
- Candidate density and pass rate.

Only after this should weights be tuned.

## 18. Reset Decision Criteria

Discard and rebuild if:

- Current code cannot cleanly separate route validity from scoring/context.
- Metadata preservation requires invasive changes anyway.
- More hard-gate edits continue lowering candidate density without improving pass rate.
- Stage-family leakage remains hard to reason about.

Refactor and preserve if:

- The existing modules can be separated into universe, data, baseline, routing, evaluation, scoring, and audit layers.
- Current Crossover logic can be simplified without breaking the UI.
- Validation scripts can be upgraded to preserve metadata and report density automatically.

## 19. Immediate Next Step

Before further signal changes, create a comparison plan:

```text
Fresh charter requirement -> Current engine behavior -> Keep / Refactor / Discard
```

This should be done module by module, not ticker by ticker.
