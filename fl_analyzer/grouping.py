from collections import defaultdict
import csv
import os


def group_by_aggregation(results):
    groups = defaultdict(list)

    for result in results:
        aggregation = result.get("aggregation", "Unknown")
        groups[aggregation].append(result)

    summaries = []

    for aggregation, experiments in sorted(groups.items()):
        count = len(experiments)

        mean_final_accuracy = sum(
            item["final_accuracy"] for item in experiments
        ) / count

        mean_best_accuracy = sum(
            item["best_accuracy"] for item in experiments
        ) / count

        mean_last_3_accuracy = sum(
            item["avg_last_3_accuracy"] for item in experiments
        ) / count

        summaries.append(
            {
                "aggregation": aggregation,
                "experiments": count,
                "mean_final_accuracy": mean_final_accuracy,
                "mean_best_accuracy": mean_best_accuracy,
                "mean_last_3_accuracy": mean_last_3_accuracy,
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
            "mean_best_accuracy",
            "mean_last_3_accuracy",
        ])

        for item in summaries:
            writer.writerow([
                item["aggregation"],
                item["experiments"],
                item["mean_final_accuracy"],
                item["mean_best_accuracy"],
                item["mean_last_3_accuracy"],
            ])