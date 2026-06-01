# Validation

Validation evidence belongs here.

Use `validation/baselines/` for accepted baseline summaries.

Use `validation/runs/` for dated experiment outputs and notes.

V3 run artifacts should use the default dated names from `stock_screener_v3.run_io` unless a test case needs an explicit override:

- `v3_backtest_YYYYMMDD_details.csv`
- `v3_backtest_YYYYMMDD_summary.md`
- `v3_backtest_YYYYMMDD.log`

Every validation run should state:

- D date or date range.
- Universe and filters.
- Symbols processed.
- Candidates found.
- Candidate density.
- Forward horizons.
- Pass rate.
- Failure categories.
