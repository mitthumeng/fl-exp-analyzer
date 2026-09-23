import sys

from fl_analyzer.parser import parse_log
from fl_analyzer.metrics import compute_summary
from fl_analyzer.visualization import plot_metrics


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <log_file>")
        return

    log_file = sys.argv[1]

    records = parse_log(log_file)

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

    plot_metrics(records)

    print("Plots saved to results/")


if __name__ == "__main__":
    main()