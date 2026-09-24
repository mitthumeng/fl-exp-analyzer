from fl_analyzer.grouping import (
    group_by_dataset_attack_aggregation,
)


def test_group_by_dataset_attack_aggregation():
    results = [
        {
            "dataset": "MNIST",
            "attack": "LabelFlipping",
            "aggregation": "FedAvg",
            "final_accuracy": 0.60,
            "best_accuracy": 0.64,
            "avg_last_3_accuracy": 0.61,
        },
        {
            "dataset": "MNIST",
            "attack": "LabelFlipping",
            "aggregation": "FedAvg",
            "final_accuracy": 0.70,
            "best_accuracy": 0.74,
            "avg_last_3_accuracy": 0.71,
        },
        {
            "dataset": "MNIST",
            "attack": "LabelFlipping",
            "aggregation": "Median",
            "final_accuracy": 0.66,
            "best_accuracy": 0.69,
            "avg_last_3_accuracy": 0.67,
        },
        {
            "dataset": "CIFAR10",
            "attack": "GradientAscent",
            "aggregation": "FedAvg",
            "final_accuracy": 0.48,
            "best_accuracy": 0.52,
            "avg_last_3_accuracy": 0.49,
        },
    ]

    summaries = group_by_dataset_attack_aggregation(results)

    assert len(summaries) == 3

    mnist_lf_fedavg = next(
        item for item in summaries
        if item["dataset"] == "MNIST"
        and item["attack"] == "LabelFlipping"
        and item["aggregation"] == "FedAvg"
    )

    assert mnist_lf_fedavg["experiments"] == 2
    assert abs(
        mnist_lf_fedavg["mean_final_accuracy"] - 0.65
    ) < 1e-8

    assert mnist_lf_fedavg["std_final_accuracy"] > 0

    mnist_lf_median = next(
        item for item in summaries
        if item["dataset"] == "MNIST"
        and item["attack"] == "LabelFlipping"
        and item["aggregation"] == "Median"
    )

    assert mnist_lf_median["experiments"] == 1
    assert mnist_lf_median["std_final_accuracy"] == 0.0


def test_unknown_dataset_attack_aggregation():
    results = [
        {
            "final_accuracy": 0.50,
            "best_accuracy": 0.55,
            "avg_last_3_accuracy": 0.52,
        }
    ]

    summaries = group_by_dataset_attack_aggregation(results)

    assert len(summaries) == 1

    item = summaries[0]

    assert item["dataset"] == "Unknown"
    assert item["attack"] == "Unknown"
    assert item["aggregation"] == "Unknown"


def test_empty_dataset_attack_aggregation():
    summaries = group_by_dataset_attack_aggregation([])

    assert summaries == []