import argparse

from fl_analyzer.registry import (
    compute_retry_counts,
    filter_runs,
    list_runs,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="List managed experiment runs."
    )

    parser.add_argument(
        "--runs-dir",
        default="runs",
        help="Directory containing managed experiment runs.",
    )

    parser.add_argument(
        "--dataset",
        help="Filter runs by dataset.",
    )

    parser.add_argument(
        "--aggregation",
        help="Filter runs by aggregation method.",
    )

    parser.add_argument(
        "--attack",
        help="Filter runs by attack type.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        help="Filter runs by random seed.",
    )

    parser.add_argument(
        "--status",
        choices=[
            "running",
            "completed",
            "failed",
            "unknown",
        ],
        help="Filter runs by execution status.",
    )

    return parser


def print_runs(runs, retry_counts):
    print(
        f"{'Run ID':<45}"
        f"{'Dataset':<12}"
        f"{'Aggregation':<16}"
        f"{'Attack':<18}"
        f"{'Seed':>8}"
        f"{'Status':>12}"
        f"{'Retries':>10}"
        f"{'Retry Of':>35}"
    )

    print("-" * 156)

    for run in runs:
        retry_count = retry_counts.get(
            run["run_id"],
            0,
        )

        retry_of = run.get("retry_of") or "-"

        print(
            f"{run['run_id']:<45}"
            f"{str(run['dataset']):<12}"
            f"{str(run['aggregation']):<16}"
            f"{str(run['attack']):<18}"
            f"{str(run['seed']):>8}"
            f"{run['status']:>12}"
            f"{retry_count:>10}"
            f"{retry_of:>35}"
        )


def main():
    parser = build_parser()
    args = parser.parse_args()

    all_runs = list_runs(
        args.runs_dir
    )

    if not all_runs:
        print("No managed runs found.")
        return

    retry_counts = compute_retry_counts(
        all_runs
    )

    runs = filter_runs(
        all_runs,
        dataset=args.dataset,
        aggregation=args.aggregation,
        attack=args.attack,
        seed=args.seed,
        status=args.status,
    )

    if not runs:
        print("No runs match the selected filters.")
        return

    print_runs(
        runs,
        retry_counts,
    )


if __name__ == "__main__":
    main()