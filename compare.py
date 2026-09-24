import argparse
from pathlib import Path

from fl_analyzer.parser import parse_log, parse_metadata
from fl_analyzer.metrics import compute_summary
from fl_analyzer.comparison import export_comparison
from fl_analyzer.grouping import (
    group_results,
    group_by_aggregation,
    group_by_dataset_and_aggregation,
    group_by_attack,
    group_by_dataset_attack_aggregation,
    export_group_summary,
    export_dataset_aggregation_summary,
    export_attack_summary,
    export_dataset_attack_aggregation_summary,
    export_custom_group_summary,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Compare multiple federated learning experiment logs "
            "and generate grouped summaries."
        )
    )

    parser.add_argument(
        "inputs",
        nargs="+",
        help="Log files or directories containing .log files.",
    )

    parser.add_argument(
        "--group-by",
        nargs="+",
        choices=[
            "dataset",
            "attack",
            "aggregation",
            "seed",
        ],
        default=["aggregation"],
        help=(
            "Fields used for the custom grouped summary. "
            "Default: aggregation"
        ),
    )

    return parser


def analyze_file(file_path):
    try:
        records = parse_log(file_path)
        metadata = parse_metadata(file_path)

    except (FileNotFoundError, ValueError) as exc:
        print(f"Warning: {exc}")
        return None

    if not records:
        print(f"Warning: no valid records found in {file_path}")
        return None

    summary = compute_summary(records)

    return {
        "name": Path(file_path).stem,
        "dataset": metadata.get("dataset", "Unknown"),
        "aggregation": metadata.get("aggregation", "Unknown"),
        "attack": metadata.get("attack", "Unknown"),
        "seed": metadata.get("seed", "Unknown"),
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
    print("\nExperiment Comparison")

    print(
        f"{'Experiment':<18}"
        f"{'Dataset':<12}"
        f"{'Aggregation':<16}"
        f"{'Attack':<18}"
        f"{'Seed':>8}"
        f"{'Final Acc':>12}"
        f"{'Best Acc':>12}"
    )

    print("-" * 96)

    for result in results:
        print(
            f"{result['name']:<18}"
            f"{str(result['dataset']):<12}"
            f"{str(result['aggregation']):<16}"
            f"{str(result['attack']):<18}"
            f"{str(result['seed']):>8}"
            f"{result['final_accuracy']:>12.4f}"
            f"{result['best_accuracy']:>12.4f}"
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


def print_dataset_aggregation_summary(summaries):
    print("\nDataset + Aggregation Summary")

    print(
        f"{'Dataset':<15}"
        f"{'Aggregation':<16}"
        f"{'N':>6}"
        f"{'Final Acc':>20}"
        f"{'Best Acc':>20}"
    )

    print("-" * 77)

    for item in summaries:
        final_text = (
            f"{item['mean_final_accuracy']:.4f} "
            f"± {item['std_final_accuracy']:.4f}"
        )

        best_text = (
            f"{item['mean_best_accuracy']:.4f} "
            f"± {item['std_best_accuracy']:.4f}"
        )

        print(
            f"{item['dataset']:<15}"
            f"{item['aggregation']:<16}"
            f"{item['experiments']:>6}"
            f"{final_text:>20}"
            f"{best_text:>20}"
        )


def print_attack_summary(summaries):
    print("\nAttack Summary")

    print(
        f"{'Attack':<20}"
        f"{'N':>6}"
        f"{'Final Acc':>20}"
        f"{'Best Acc':>20}"
    )

    print("-" * 66)

    for item in summaries:
        final_text = (
            f"{item['mean_final_accuracy']:.4f} "
            f"± {item['std_final_accuracy']:.4f}"
        )

        best_text = (
            f"{item['mean_best_accuracy']:.4f} "
            f"± {item['std_best_accuracy']:.4f}"
        )

        print(
            f"{item['attack']:<20}"
            f"{item['experiments']:>6}"
            f"{final_text:>20}"
            f"{best_text:>20}"
        )


def print_dataset_attack_aggregation_summary(summaries):
    print("\nDataset + Attack + Aggregation Summary")

    print(
        f"{'Dataset':<12}"
        f"{'Attack':<18}"
        f"{'Aggregation':<16}"
        f"{'N':>6}"
        f"{'Final Acc':>20}"
        f"{'Best Acc':>20}"
    )

    print("-" * 92)

    for item in summaries:
        final_text = (
            f"{item['mean_final_accuracy']:.4f} "
            f"± {item['std_final_accuracy']:.4f}"
        )

        best_text = (
            f"{item['mean_best_accuracy']:.4f} "
            f"± {item['std_best_accuracy']:.4f}"
        )

        print(
            f"{item['dataset']:<12}"
            f"{item['attack']:<18}"
            f"{item['aggregation']:<16}"
            f"{item['experiments']:>6}"
            f"{final_text:>20}"
            f"{best_text:>20}"
        )


def print_custom_group_summary(summaries, keys):
    print(
        "\nCustom Group Summary "
        f"({', '.join(keys)})"
    )

    key_width = 16

    header = ""

    for key in keys:
        header += f"{key.title():<{key_width}}"

    header += (
        f"{'N':>6}"
        f"{'Final Acc':>20}"
        f"{'Best Acc':>20}"
        f"{'Last 3 Acc':>20}"
    )

    print(header)
    print("-" * len(header))

    for item in summaries:
        row = ""

        for key in keys:
            row += f"{str(item[key]):<{key_width}}"

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

        row += (
            f"{item['experiments']:>6}"
            f"{final_text:>20}"
            f"{best_text:>20}"
            f"{last_3_text:>20}"
        )

        print(row)


def main():
    parser = build_parser()
    args = parser.parse_args()

    log_files = collect_log_files(args.inputs)

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

    # Individual experiment comparison
    print_comparison(results)

    # Aggregation-level summary
    aggregation_results = group_by_aggregation(results)
    print_group_summary(aggregation_results)

    # Dataset + aggregation summary
    dataset_aggregation_results = (
        group_by_dataset_and_aggregation(results)
    )
    print_dataset_aggregation_summary(
        dataset_aggregation_results
    )

    # Attack-level summary
    attack_results = group_by_attack(results)
    print_attack_summary(attack_results)

    # Dataset + attack + aggregation summary
    dataset_attack_aggregation_results = (
        group_by_dataset_attack_aggregation(results)
    )
    print_dataset_attack_aggregation_summary(
        dataset_attack_aggregation_results
    )

    # User-configurable grouping
    custom_group_results = group_results(
        results,
        keys=args.group_by,
    )

    print_custom_group_summary(
        custom_group_results,
        args.group_by,
    )

    # Export CSV files
    export_comparison(results)

    export_group_summary(
        aggregation_results
    )

    export_dataset_aggregation_summary(
        dataset_aggregation_results
    )

    export_attack_summary(
        attack_results
    )

    export_dataset_attack_aggregation_summary(
        dataset_attack_aggregation_results
    )

    print("\nCSV files generated:")
    print("  results/comparison.csv")
    print("  results/aggregation_summary.csv")
    print("  results/dataset_aggregation_summary.csv")
    print("  results/attack_summary.csv")
    print(
        "  results/"
        "dataset_attack_aggregation_summary.csv"
    )

    custom_filename = (
        "results/group_by_"
        + "_".join(args.group_by)
        + ".csv"
    )

    export_custom_group_summary(
        custom_group_results,
        args.group_by,
        custom_filename,
    )

    print(f"  {custom_filename}")


if __name__ == "__main__":
    main()