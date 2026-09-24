import argparse

from fl_analyzer.parser import parse_log
from fl_analyzer.metrics import compute_summary
from fl_analyzer.visualization import plot_metrics
from fl_analyzer.exporter import export_summary


def build_parser():
    parser = argparse.ArgumentParser(
        description="Analyze a federated learning experiment log."
    )

    parser.add_argument(
        "log_file",
        help="Path to the experiment log file.",
    )

    parser.add_argument(
        "--output",
        default="results",
        help="Directory used to store plots and CSV output.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        records = parse_log(args.log_file)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        return

    if not records:
        print("No valid experiment records found.")
        return

    summary = compute_summary(records)

    print(f"Rounds: {summary['rounds']}")
    print(f"Final Accuracy: {summary['final_accuracy']:.4f}")
    print(f"Best Accuracy: {summary['best_accuracy']:.4f}")
    print(f"Best Round: {summary['best_round']}")
    print(
        f"Average Accuracy (Last 3 Rounds): "
        f"{summary['avg_last_3_accuracy']:.4f}"
    )

    plot_metrics(records, output_dir=args.output)

    summary_path = f"{args.output}/summary.csv"
    export_summary(summary, output_path=summary_path)

    print(f"Plots saved to {args.output}/")
    print(f"Summary saved to {summary_path}")


if __name__ == "__main__":
    main()