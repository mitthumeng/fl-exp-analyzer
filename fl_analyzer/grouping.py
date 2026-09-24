from collections import defaultdict


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