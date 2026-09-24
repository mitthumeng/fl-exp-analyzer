import sys
from pathlib import Path

from fl_analyzer.parser import parse_log
from fl_analyzer.metrics import compute_summary


def analyze_file(file_path):
    try:
        records = parse_log(file_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Warning: {exc}")
        return None

    if not records:
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
    if len(sys.argv) < 3:
        print("Usage: python compare.py <log_file_1> <log_file_2> [...]")
        return

    results = []

    for file_path in sys.argv[1:]:
        result = analyze_file(file_path)

        if result is None:
            print(f"Warning: no valid records found in {file_path}")
            continue

        results.append(result)

    if not results:
        print("No valid experiments found.")
        return

    print_comparison(results)


if __name__ == "__main__":
    main()