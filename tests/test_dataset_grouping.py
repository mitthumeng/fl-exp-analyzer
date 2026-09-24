from fl_analyzer.grouping import group_by_dataset_and_aggregation


def test_group_by_dataset_and_aggregation():
    results = [
        {
            "dataset": "MNIST",
            "aggregation": "FedAvg",
            "final_accuracy": 0.60,
            "best_accuracy": 0.65,
            "avg_last_3_accuracy": 0.62,
        },
        {
            "dataset": "MNIST",
            "aggregation": "FedAvg",
            "final_accuracy": 0.70,
            "best_accuracy": 0.74,
            "avg_last_3_accuracy": 0.71,
        },
        {
            "dataset": "CIFAR10",
            "aggregation": "FedAvg",
            "final_accuracy": 0.50,
            "best_accuracy": 0.55,
            "avg_last_3_accuracy": 0.52,
        },
        {
            "dataset": "MNIST",
            "aggregation": "Median",
            "final_accuracy": 0.66,
            "best_accuracy": 0.69,
            "avg_last_3_accuracy": 0.67,
        },
    ]

    summaries = group_by_dataset_and_aggregation(results)

    assert len(summaries) == 3

    mnist_fedavg = next(
        item for item in summaries
        if item["dataset"] == "MNIST"
        and item["aggregation"] == "FedAvg"
    )

    cifar_fedavg = next(
        item for item in summaries
        if item["dataset"] == "CIFAR10"
        and item["aggregation"] == "FedAvg"
    )

    mnist_median = next(
        item for item in summaries
        if item["dataset"] == "MNIST"
        and item["aggregation"] == "Median"
    )

    assert mnist_fedavg["experiments"] == 2
    assert abs(
        mnist_fedavg["mean_final_accuracy"] - 0.65
    ) < 1e-8

    assert cifar_fedavg["experiments"] == 1
    assert cifar_fedavg["mean_final_accuracy"] == 0.50

    assert mnist_median["experiments"] == 1
    assert mnist_median["mean_final_accuracy"] == 0.66


def test_unknown_dataset_and_aggregation():
    results = [
        {
            "final_accuracy": 0.50,
            "best_accuracy": 0.55,
            "avg_last_3_accuracy": 0.52,
        }
    ]

    summaries = group_by_dataset_and_aggregation(results)

    assert len(summaries) == 1
    assert summaries[0]["dataset"] == "Unknown"
    assert summaries[0]["aggregation"] == "Unknown"


def test_empty_dataset_aggregation_results():
    summaries = group_by_dataset_and_aggregation([])

    assert summaries == []