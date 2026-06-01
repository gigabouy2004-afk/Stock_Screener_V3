# Backtesting Engine Requirements

Date: 2026-06-01

The backtesting engine is a first-class deliverable for this rebuild.

## Purpose

Run the production signal engine as of a historical D date and validate the resulting candidates against future bars that were unavailable on D.

## Core Requirements

- Execute the same signal engine used by live scans.
- Prevent look-ahead bias.
- Preserve universe metadata.
- Support deterministic random samples.
- Support sector-filtered samples.
- Support full-universe ranked runs.
- Report candidate density.
- Report D+1, D+2, and D+5 results.
- Produce detail CSV and summary markdown.
- Produce aggregate comparison scorecards.

## V1 Foundation Status

Implemented foundation pieces:

- Backtest engine shell.
- Price provider protocol.
- Stage evaluator protocol.
- In-memory price provider for tests.
- Historical as-of slicing.
- Candidate-density calculation.
- Candidate-only forward hit-rate summary.

Not yet implemented:

- Production data provider.
- Production stage evaluators.
- Detail CSV writer.
- Summary markdown writer.
- Multi-date scorecards.
- Failure-category classification.

## Required Run Modes

| Mode | Purpose |
|---|---|
| Single-date replay | Debug one D date |
| Multi-date replay | Validate across regimes |
| Random-lot replay | Avoid cherry-picking |
| Full-universe ranked replay | Simulate real scanner behavior |

## Required Output Metrics

- Universe size.
- Symbols processed.
- Symbols skipped.
- Skip reasons.
- Candidates found.
- Candidate density.
- D+1 hit rate.
- D+2 hit rate.
- D+5 hit rate.
- Average forward return.
- Median forward return.
- Pass rate by sector.
- Pass rate by score bucket.
- Pass rate by review priority.
- Failure reason-code distribution.

## Anti-Bias Rules

- Do not use future bars in signal generation.
- Do not use current profile metadata as historical truth without tagging it.
- Do not report only winners.
- Do not hide skipped symbols.
- Do not compare first-N-candidate tests against ranked full-universe tests as equivalent.
- Do not tune rules from a single ticker.
