import argparse

from fl_analyzer.registry import (
    list_runs,
    filter_runs,
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


def main():
    parser = build_parser()
    args = parser.parse_args()

    runs = list_runs(args.runs_dir)
    runs = filter_runs(
    runs,
    dataset=args.dataset,
    aggregation=args.aggregation,
    attack=args.attack,
    seed=args.seed,
    status=args.status,
)

    if not runs:
        print("No managed runs found.")
        return

    print(
        f"{'Run ID':<45}"
        f"{'Dataset':<12}"
        f"{'Aggregation':<16}"
        f"{'Attack':<18}"
        f"{'Seed':>8}"
        f"{'Status':>12}"
    )

    print("-" * 111)

    for run in runs:
        print(
            f"{run['run_id']:<45}"
            f"{str(run['dataset']):<12}"
            f"{str(run['aggregation']):<16}"
            f"{str(run['attack']):<18}"
            f"{str(run['seed']):>8}"
            f"{run['status']:>12}"
        )


if __name__ == "__main__":
    main()