import argparse

from fl_analyzer.retry_policy import (
    RetryPolicy,
    retry_with_policy,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Automatically retry a failed managed "
            "experiment."
        )
    )

    parser.add_argument(
        "run_dir",
        help="Path to the failed experiment run.",
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help=(
            "Maximum number of retry attempts. "
            "Default: 3"
        ),
    )

    parser.add_argument(
        "--runs-dir",
        default="runs",
        help="Directory used to store retry runs.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    policy = RetryPolicy(
        max_retries=args.max_retries
    )

    try:
        result = retry_with_policy(
            args.run_dir,
            policy,
            base_dir=args.runs_dir,
        )

    except (
        FileNotFoundError,
        ValueError,
    ) as exc:
        print(f"Error: {exc}")
        return

    print(
        f"Final status: {result['status']}"
    )

    print(
        f"Retry attempts: "
        f"{len(result['attempts'])}"
    )

    for attempt in result["attempts"]:
        print(
            f"Attempt {attempt['attempt']}: "
            f"{attempt['source_run']} "
            f"-> {attempt['new_run']} "
            f"({attempt['status']}, "
            f"return_code="
            f"{attempt['return_code']})"
        )

    print(
        f"Final run: {result['final_run']}"
    )


if __name__ == "__main__":
    main()