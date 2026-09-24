from fl_analyzer.grouping import group_by_aggregation


def test_group_by_aggregation():
    results = [
        {
            "aggregation": "FedAvg",
            "final_accuracy": 0.60,
            "best_accuracy": 0.65,
            "avg_last_3_accuracy": 0.62,
        },
        {
            "aggregation": "FedAvg",
            "final_accuracy": 0.70,
            "best_accuracy": 0.74,
            "avg_last_3_accuracy": 0.71,
        },
        {
            "aggregation": "Median",
            "final_accuracy": 0.66,
            "best_accuracy": 0.69,
            "avg_last_3_accuracy": 0.67,
        },
    ]

    summaries = group_by_aggregation(results)

    assert len(summaries) == 2

    fedavg = next(
        item for item in summaries
        if item["aggregation"] == "FedAvg"
    )

    median = next(
        item for item in summaries
        if item["aggregation"] == "Median"
    )

    assert fedavg["experiments"] == 2
    assert abs(fedavg["mean_final_accuracy"] - 0.65) < 1e-8
    assert abs(fedavg["mean_best_accuracy"] - 0.695) < 1e-8
    assert abs(fedavg["mean_last_3_accuracy"] - 0.665) < 1e-8

    assert median["experiments"] == 1
    assert median["mean_final_accuracy"] == 0.66
    assert median["mean_best_accuracy"] == 0.69
    assert median["mean_last_3_accuracy"] == 0.67


def test_unknown_aggregation():
    results = [
        {
            "final_accuracy": 0.50,
            "best_accuracy": 0.55,
            "avg_last_3_accuracy": 0.52,
        }
    ]

    summaries = group_by_aggregation(results)

    assert len(summaries) == 1
    assert summaries[0]["aggregation"] == "Unknown"
    assert summaries[0]["experiments"] == 1


def test_empty_results():
    summaries = group_by_aggregation([])

    assert summaries == []