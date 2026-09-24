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

def group_by_dataset_and_aggregation(results):
    groups = defaultdict(list)

    for result in results:
        dataset = result.get("dataset", "Unknown")
        aggregation = result.get("aggregation", "Unknown")

        groups[(dataset, aggregation)].append(result)

    summaries = []

    for (dataset, aggregation), experiments in sorted(groups.items()):
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

        summaries.append(
            {
                "dataset": dataset,
                "aggregation": aggregation,
                "experiments": count,
                "mean_final_accuracy": statistics.mean(final_accuracies),
                "std_final_accuracy": (
                    statistics.stdev(final_accuracies)
                    if count > 1 else 0.0
                ),
                "mean_best_accuracy": statistics.mean(best_accuracies),
                "std_best_accuracy": (
                    statistics.stdev(best_accuracies)
                    if count > 1 else 0.0
                ),
                "mean_last_3_accuracy": statistics.mean(last_3_accuracies),
                "std_last_3_accuracy": (
                    statistics.stdev(last_3_accuracies)
                    if count > 1 else 0.0
                ),
            }
        )

    return summaries

def export_dataset_aggregation_summary(
    summaries,
    output_path="results/dataset_aggregation_summary.csv",
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "dataset",
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
                item["dataset"],
                item["aggregation"],
                item["experiments"],
                item["mean_final_accuracy"],
                item["std_final_accuracy"],
                item["mean_best_accuracy"],
                item["std_best_accuracy"],
                item["mean_last_3_accuracy"],
                item["std_last_3_accuracy"],
            ])

def group_by_attack(results):
    groups = defaultdict(list)

    for result in results:
        attack = result.get("attack", "Unknown")
        groups[attack].append(result)

    summaries = []

    for attack, experiments in sorted(groups.items()):
        count = len(experiments)

        final_accuracies = [
            item["final_accuracy"] for item in experiments
        ]
        best_accuracies = [
            item["best_accuracy"] for item in experiments
        ]

        summaries.append(
            {
                "attack": attack,
                "experiments": count,
                "mean_final_accuracy": statistics.mean(final_accuracies),
                "std_final_accuracy": (
                    statistics.stdev(final_accuracies)
                    if count > 1 else 0.0
                ),
                "mean_best_accuracy": statistics.mean(best_accuracies),
                "std_best_accuracy": (
                    statistics.stdev(best_accuracies)
                    if count > 1 else 0.0
                ),
            }
        )

    return summaries

def export_attack_summary(
    summaries,
    output_path="results/attack_summary.csv",
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "attack",
            "experiments",
            "mean_final_accuracy",
            "std_final_accuracy",
            "mean_best_accuracy",
            "std_best_accuracy",
        ])

        for item in summaries:
            writer.writerow([
                item["attack"],
                item["experiments"],
                item["mean_final_accuracy"],
                item["std_final_accuracy"],
                item["mean_best_accuracy"],
                item["std_best_accuracy"],
            ])

def group_by_dataset_attack_aggregation(results):
    groups = defaultdict(list)

    for result in results:
        dataset = result.get("dataset", "Unknown")
        attack = result.get("attack", "Unknown")
        aggregation = result.get("aggregation", "Unknown")

        groups[(dataset, attack, aggregation)].append(result)

    summaries = []

    for (dataset, attack, aggregation), experiments in sorted(groups.items()):
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

        summaries.append(
            {
                "dataset": dataset,
                "attack": attack,
                "aggregation": aggregation,
                "experiments": count,
                "mean_final_accuracy": statistics.mean(final_accuracies),
                "std_final_accuracy": (
                    statistics.stdev(final_accuracies)
                    if count > 1 else 0.0
                ),
                "mean_best_accuracy": statistics.mean(best_accuracies),
                "std_best_accuracy": (
                    statistics.stdev(best_accuracies)
                    if count > 1 else 0.0
                ),
                "mean_last_3_accuracy": statistics.mean(last_3_accuracies),
                "std_last_3_accuracy": (
                    statistics.stdev(last_3_accuracies)
                    if count > 1 else 0.0
                ),
            }
        )

    return summaries

def export_dataset_attack_aggregation_summary(
    summaries,
    output_path="results/dataset_attack_aggregation_summary.csv",
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "dataset",
            "attack",
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
                item["dataset"],
                item["attack"],
                item["aggregation"],
                item["experiments"],
                item["mean_final_accuracy"],
                item["std_final_accuracy"],
                item["mean_best_accuracy"],
                item["std_best_accuracy"],
                item["mean_last_3_accuracy"],
                item["std_last_3_accuracy"],
            ])

def group_results(results, keys):
    groups = defaultdict(list)

    for result in results:
        group_key = tuple(
            result.get(key, "Unknown")
            for key in keys
        )
        groups[group_key].append(result)

    summaries = []

    for group_key, experiments in sorted(groups.items()):
        count = len(experiments)

        final_accuracies = [
            item["final_accuracy"]
            for item in experiments
        ]
        best_accuracies = [
            item["best_accuracy"]
            for item in experiments
        ]
        last_3_accuracies = [
            item["avg_last_3_accuracy"]
            for item in experiments
        ]

        summary = {
            key: value
            for key, value in zip(keys, group_key)
        }

        summary.update({
            "experiments": count,
            "mean_final_accuracy": statistics.mean(final_accuracies),
            "std_final_accuracy": (
                statistics.stdev(final_accuracies)
                if count > 1 else 0.0
            ),
            "mean_best_accuracy": statistics.mean(best_accuracies),
            "std_best_accuracy": (
                statistics.stdev(best_accuracies)
                if count > 1 else 0.0
            ),
            "mean_last_3_accuracy": statistics.mean(last_3_accuracies),
            "std_last_3_accuracy": (
                statistics.stdev(last_3_accuracies)
                if count > 1 else 0.0
            ),
        })

        summaries.append(summary)

    return summaries

def group_by_aggregation(results):
    return group_results(
        results,
        keys=["aggregation"],
    )


def group_by_attack(results):
    return group_results(
        results,
        keys=["attack"],
    )


def group_by_dataset_and_aggregation(results):
    return group_results(
        results,
        keys=["dataset", "aggregation"],
    )


def group_by_dataset_attack_aggregation(results):
    return group_results(
        results,
        keys=["dataset", "attack", "aggregation"],
    )

def export_custom_group_summary(
    summaries,
    keys,
    output_path,
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = (
        list(keys)
        + [
            "experiments",
            "mean_final_accuracy",
            "std_final_accuracy",
            "mean_best_accuracy",
            "std_best_accuracy",
            "mean_last_3_accuracy",
            "std_last_3_accuracy",
        ]
    )

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for item in summaries:
            writer.writerow({
                field: item[field]
                for field in fieldnames
            })