import argparse
import shlex

from fl_analyzer.config import load_config
from fl_analyzer.runner import run_experiment


def build_parser():
    parser = argparse.ArgumentParser(
        description="Run a managed experiment."
    )

    parser.add_argument(
        "config",
        help="Path to the experiment YAML configuration.",
    )

    parser.add_argument(
        "--command",
        required=True,
        help="Command used to execute the experiment.",
    )

    parser.add_argument(
        "--runs-dir",
        default="runs",
        help="Directory used to store managed runs.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.config)

    command = shlex.split(args.command)

    run_dir, status = run_experiment(
        config,
        command,
        base_dir=args.runs_dir,
    )

    print(f"Run directory: {run_dir}")
    print(f"Status: {status['status']}")
    print(f"Return code: {status['return_code']}")


if __name__ == "__main__":
    main()