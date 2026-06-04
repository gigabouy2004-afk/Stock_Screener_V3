from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from stock_screener_v3.runner import run_backtest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stock Screener V3 engine runner.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backtest = subparsers.add_parser("backtest", help="Run the V3 engine as of a historical D date.")
    backtest.add_argument("--workspace-root", default=str(Path.cwd()), help="Workspace root for input/output paths.")
    backtest.add_argument("--universe-file", required=True, help="CSV universe file inside the workspace.")
    backtest.add_argument("--d-date", required=True, help="Engine execution date in YYYY-MM-DD format.")
    backtest.add_argument("--sector", default="", help="Comma-separated sector filters.")
    backtest.add_argument("--exchange", default="", help="Comma-separated exchange filters.")
    backtest.add_argument("--sample-size", type=int, default=None, help="Optional deterministic random sample size.")
    backtest.add_argument("--random-seed", type=int, default=None, help="Optional deterministic random seed.")
    backtest.add_argument("--forward-days", default="1,2,5", help="Comma-separated forward validation horizons.")
    backtest.add_argument("--stage-family", default="CROSSOVER,MOMENTUM_SETUP,DIVERGENCE", help="Comma-separated stage families.")
    backtest.add_argument("--run-label", default="v3_backtest", help="Artifact filename prefix.")
    backtest.add_argument("--details-output", default=None, help="Optional detail CSV path.")
    backtest.add_argument("--summary-output", default=None, help="Optional summary markdown path.")
    backtest.add_argument("--log-file", default=None, help="Optional execution summary log path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "backtest":
        result = run_backtest(
            workspace_root=args.workspace_root,
            universe_file=args.universe_file,
            d_date=date.fromisoformat(args.d_date),
            sectors=_split_csv(args.sector),
            exchanges=_split_csv(args.exchange),
            sample_size=args.sample_size,
            random_seed=args.random_seed,
            forward_days=tuple(int(value) for value in _split_csv(args.forward_days)),
            stage_families=_split_csv(args.stage_family),
            run_label=args.run_label,
            details_output=args.details_output,
            summary_output=args.summary_output,
            log_file=args.log_file,
        )
        print(f"Processed: {result.result.symbols_processed}")
        print(f"Candidates: {result.result.candidates_found}")
        print(f"Output CSV: {result.paths.details_output}")
        print(f"Summary: {result.paths.summary_output}")
        print(f"Log: {result.paths.log_file}")
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())


if __name__ == "__main__":
    raise SystemExit(main())

