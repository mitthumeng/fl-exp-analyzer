import sys
from pathlib import Path

from fl_analyzer.parser import parse_log
from fl_analyzer.metrics import compute_summary
from fl_analyzer.comparison import export_comparison


def analyze_file(file_path):
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

    export_comparison(results)
    print("Comparison saved to results/comparison.csv")


if __name__ == "__main__":
    main()