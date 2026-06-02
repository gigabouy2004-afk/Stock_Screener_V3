# V3 Module Contracts

Date: 2026-06-01

This document defines the first-pass module contracts for the V3 engine.

## 1. Universe Module

Responsibility:

Load symbols and metadata.

Output model:

```text
UniverseRecord
```

Required fields:

- symbol.
- yahoo_symbol.
- company_name.
- exchange.
- sector.
- industry.
- instrument_type.
- market_cap.
- avg_daily_volume.
- source_file.
- last_profile_refresh_date.

Input contract:

- The primary input is a CSV universe file.
- A single CSV may contain mixed NSE, BSE, NYSE, and NASDAQ stock codes.
- `Symbol` or `Ticker` is required.
- `Exchange` should be provided when symbols are not already Yahoo-normalized.
- NSE symbols without a suffix normalize to `.NS`.
- BSE symbols without a suffix normalize to `.BO`.
- NYSE and NASDAQ symbols remain unsuffixed unless `YahooSymbol` is explicitly provided.
- `YahooSymbol` or `Yahoo Symbol` overrides automatic normalization.

Non-responsibilities:

- Fetching prices.
- Calculating indicators.
- Classifying candidates.

## 2. Data Provider Module

Responsibility:

Fetch and normalize OHLCV and benchmark data.

Output model:

```text
PriceDataBundle
```

Required behavior:

- Daily data.
- Intraday data.
- Benchmark data.
- Structured missing-data errors.
- Historical as-of slicing.

Non-responsibilities:

- Candidate classification.
- Scoring.
- Output ranking.

## 3. Evidence Module

Responsibility:

Convert price data into neutral technical facts.

Output model:

```text
EvidencePack
```

Evidence sections:

- market_context.
- sector_context.
- stock_baseline.
- momentum.
- trend.
- volatility.
- volume.
- structure.
- risk_context.

Non-responsibilities:

- CandidateState.
- CandidateClass.
- ReviewPriority.

## 4. Stage Evaluator Module

Responsibility:

Evaluate evidence against stage-family definitions.

Output model:

```text
StageEvaluation
```

Required fields:

- candidate_state.
- candidate_class.
- review_priority.
- confidence.
- score_components.
- reason_codes.
- risk_tags.

Stage family boundaries:

- `CROSSOVER` is for phase-transition evidence:
  - `PRE_BULL_CROSSOVER`: seller-to-buyer transition / new capital entry review.
  - `PRE_BEAR_CROSSOVER`: buyer-to-seller transition / exit and capital-preservation review.
- `MOMENTUM_SETUP` is for bull-phase continuation or re-entry after the bullish phase already exists:
  - `BULL_PULLBACK_REENTRY`.
  - `BULL_CONTINUATION_MOMENTUM`.
- `DIVERGENCE` is for price/momentum disagreement and remains a separate evaluator family.

Non-responsibilities:

- Fetching data.
- Writing reports.
- Historical forward validation.

## 5. Scoring Module

Responsibility:

Convert stage evidence into calibrated component scores.

Output model:

```text
ScoreResult
```

Required fields:

- total_score.
- route_score.
- timing_score.
- structure_score.
- participation_score.
- context_score.
- risk_score.
- labels.

## 6. Backtesting Module

Responsibility:

Run the production engine as of historical D dates and validate forward outcomes.

Output model:

```text
BacktestResult
```

Required outputs:

- detail rows.
- summary metrics.
- candidate density.
- forward returns.
- score-bucket analysis.
- failure categories.

## 7. Output Module

Responsibility:

Convert evaluations into CSV, markdown, HTML, or UI rows.

Required behavior:

- Preserve the V2-compatible offline CSV column block defined by `V2_COMPAT_EXPORT_COLUMNS`.
- Preserve the V2-compatible visible UI diagnostic column baseline defined by `V2_COMPAT_UI_COLUMNS`.
- Append V3-specific fields after the V2-compatible CSV block.
- Write CSV headers even when no candidate rows are produced.
- Keep run logs, detail CSV, and summary reports as physically separate first-class artifacts.
- Treat the log as the execution summary report and the CSV as symbol-level forensic calculation evidence.

Non-responsibilities:

- Reclassifying candidates.
- Applying hidden gates.
- Mutating scores.
