# Rebuild Way Forward Plan

Date: 2026-06-01

This plan translates the fresh charter into implementation phases.

## Phase 1: Repository Baseline

Goal: create a clean, Git-tracked reset workspace.

Deliverables:

- Fresh charter.
- Current engine gap analysis.
- Archived reference documents.
- Repository structure.
- Initial commit.

## Phase 2: Metadata Baseline

Goal: stop depending on live profile calls for basic scanner metadata.

Deliverables:

- `UniverseRecord` schema.
- Enriched US universe file.
- Enriched NSE universe file.
- Loader that returns symbol plus metadata.
- Metadata preservation in historical replay.

Required fields:

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

## Phase 3: Backtesting Engine V1

Goal: make historical validation a first-class subsystem.

Deliverables:

- Single-date replay.
- Random-lot replay.
- Sector-filtered replay.
- Full-universe ranked replay.
- D+1, D+2, and D+5 validation.
- Candidate-density reporting.
- Score-bucket reporting.
- Baseline comparison output.

Rules:

- No look-ahead bias.
- Same production engine as live scan.
- Preserve as-of metadata.
- Record all skipped symbols and reasons.

## Phase 4: Evidence Pack

Goal: separate calculations from decisions.

Deliverables:

- `EvidencePack` object.
- Market context section.
- Sector context section.
- Stock baseline section.
- Stage-specific evidence sections.
- Risk/context evidence section.

No classification should happen inside raw indicator calculation.

## Phase 5: Stage Evaluators

Goal: rebuild the decision layer around route, timing, quality, and context.

Deliverables:

- `CrossoverEvaluator`.
- `DivergenceEvaluator`.
- `MomentumEvaluator`.
- `StageEvaluation` output model.

Each evaluator should return:

- CandidateState.
- CandidateClass.
- ReviewPriority.
- Confidence.
- Score components.
- Reason codes.

## Phase 6: Crossover V2

Goal: avoid overloading one Pre-Bull state.

Candidate opportunity types:

- Below-zero bullish reversal crossover.
- Above-zero bullish pullback re-entry.
- Bullish continuation momentum.
- Above-zero bearish reversal crossover.

The engine should not hide valid technical signals merely because they carry context risk.

## Phase 7: Validation Pack

Goal: promote changes only after broad validation.

Minimum pack:

- At least 5 D dates.
- Multiple market regimes.
- Sector-restricted samples.
- Random samples.
- Large or full-universe ranked test.
- Baseline comparison.

Promotion criteria:

- Candidate density is useful.
- Score buckets separate outcomes better than baseline.
- Failure causes are explainable.
- Improvement is not isolated to one date or one ticker.

