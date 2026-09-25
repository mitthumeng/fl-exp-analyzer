import argparse

from fl_analyzer.retry import retry_run


def build_parser():
    parser = argparse.ArgumentParser(
        description="Retry a failed managed experiment."
    )

    parser.add_argument(
        "run_dir",
        help="Path to a failed run directory.",
    )

    parser.add_argument(
        "--runs-dir",
        default="runs",
        help="Directory used to store the retried run.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        new_run_dir, status = retry_run(
            args.run_dir,
            base_dir=args.runs_dir,
        )

    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        return

    print(f"Retried run created: {new_run_dir}")
    print(f"Status: {status['status']}")
    print(f"Return code: {status['return_code']}")


if __name__ == "__main__":
    main()