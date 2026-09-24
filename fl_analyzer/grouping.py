from collections import defaultdict
import csv
import os
import statistics


def group_by_aggregation(results):
    groups = defaultdict(list)

    for result in results:
        aggregation = result.get("aggregation", "Unknown")
        groups[aggregation].append(result)

    summaries = []

    for aggregation, experiments in sorted(groups.items()):
        count = len(experiments)

        final_accuracies = [
            item["final_accuracy"] for item in experiments
        ]
        best_accuracies = [
            item["best_accuracy"] for item in experiments
        ]
        last_3_accuracies = [
            item["avg_last_3_accuracy"] for item in experiments
        ]

        mean_final_accuracy = statistics.mean(final_accuracies)
        mean_best_accuracy = statistics.mean(best_accuracies)
        mean_last_3_accuracy = statistics.mean(last_3_accuracies)

        std_final_accuracy = (
            statistics.stdev(final_accuracies)
            if count > 1 else 0.0
        )

        std_best_accuracy = (
            statistics.stdev(best_accuracies)
            if count > 1 else 0.0
        )

        std_last_3_accuracy = (
            statistics.stdev(last_3_accuracies)
            if count > 1 else 0.0
        )

        summaries.append(
            {
                "aggregation": aggregation,
                "experiments": count,
                "mean_final_accuracy": mean_final_accuracy,
                "std_final_accuracy": std_final_accuracy,
                "mean_best_accuracy": mean_best_accuracy,
                "std_best_accuracy": std_best_accuracy,
                "mean_last_3_accuracy": mean_last_3_accuracy,
                "std_last_3_accuracy": std_last_3_accuracy,
            }
        )

    return summaries

def export_group_summary(
    summaries,
    output_path="results/aggregation_summary.csv",
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "aggregation",
            "experiments",
            "mean_final_accuracy",
            "std_final_accuracy",
            "mean_best_accuracy",
            "std_best_accuracy",
            "mean_last_3_accuracy",
            "std_last_3_accuracy",
        ])

        for item in summaries:
            writer.writerow([
                item["aggregation"],
                item["experiments"],
                item["mean_final_accuracy"],
                item["std_final_accuracy"],
                item["mean_best_accuracy"],
                item["std_best_accuracy"],
                item["mean_last_3_accuracy"],
                item["std_last_3_accuracy"],
            ])