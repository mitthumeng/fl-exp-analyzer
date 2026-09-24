import sys
from pathlib import Path

from fl_analyzer.parser import parse_log
from fl_analyzer.metrics import compute_summary
from fl_analyzer.comparison import export_comparison
from fl_analyzer.parser import parse_log, parse_metadata
from fl_analyzer.grouping import (
    group_by_aggregation,
    export_group_summary,
)


def analyze_file(file_path):
    metadata = parse_metadata(file_path)
    try:
        records = parse_log(file_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Warning: {exc}")
        return None

    if not records:
        print(f"Warning: no valid records found in {file_path}")
        return None

    summary = compute_summary(records)

    return {
        "name": Path(file_path).stem,
        "rounds": summary["rounds"],
        "final_accuracy": summary["final_accuracy"],
        "best_accuracy": summary["best_accuracy"],
        "best_round": summary["best_round"],
        "avg_last_3_accuracy": summary["avg_last_3_accuracy"],
        "dataset": metadata.get("dataset", "Unknown"),
        "aggregation": metadata.get("aggregation", "Unknown"),
        "attack": metadata.get("attack", "Unknown"),
        "seed": metadata.get("seed", "Unknown"),
    }


def collect_log_files(inputs):
    log_files = []

    for item in inputs:
        path = Path(item)

        if path.is_dir():
            log_files.extend(sorted(path.glob("*.log")))
        else:
            log_files.append(path)

    return log_files


def print_comparison(results):
    print(
        f"{'Experiment':<20}"
        f"{'Rounds':>8}"
        f"{'Final Acc':>12}"
        f"{'Best Acc':>12}"
        f"{'Best Round':>12}"
        f"{'Avg Last 3':>12}"
    )

    print("-" * 76)

    for result in results:
        print(
            f"{result['name']:<20}"
            f"{result['rounds']:>8}"
            f"{result['final_accuracy']:>12.4f}"
            f"{result['best_accuracy']:>12.4f}"
            f"{result['best_round']:>12}"
            f"{result['avg_last_3_accuracy']:>12.4f}"
        )

def print_group_summary(grouped_results):
    print("\nAggregation Summary")

    print(
        f"{'Aggregation':<16}"
        f"{'N':>6}"
        f"{'Final Acc':>20}"
        f"{'Best Acc':>20}"
        f"{'Last 3 Acc':>20}"
    )

    print("-" * 82)

    for item in grouped_results:
        final_text = (
            f"{item['mean_final_accuracy']:.4f} "
            f"± {item['std_final_accuracy']:.4f}"
        )

        best_text = (
            f"{item['mean_best_accuracy']:.4f} "
            f"± {item['std_best_accuracy']:.4f}"
        )

        last_3_text = (
            f"{item['mean_last_3_accuracy']:.4f} "
            f"± {item['std_last_3_accuracy']:.4f}"
        )

        print(
            f"{item['aggregation']:<16}"
            f"{item['experiments']:>6}"
            f"{final_text:>20}"
            f"{best_text:>20}"
            f"{last_3_text:>20}"
        )

def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python compare.py "
            "<log_file_or_directory> [more_files_or_directories ...]"
        )
        return

    log_files = collect_log_files(sys.argv[1:])

    if not log_files:
        print("No log files found.")
        return

    results = []

    for file_path in log_files:
        result = analyze_file(file_path)

        if result is not None:
            results.append(result)

    if not results:
        print("No valid experiments found.")
        return

    print_comparison(results)

    grouped_results = group_by_aggregation(results)
    print_group_summary(grouped_results)

    export_comparison(results)
    export_group_summary(grouped_results)

    print("Comparison saved to results/comparison.csv")
    print(
        "Aggregation summary saved to "
        "results/aggregation_summary.csv"
    )


if __name__ == "__main__":
    main()