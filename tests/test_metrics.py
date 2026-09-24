from fl_analyzer.metrics import compute_summary


def test_compute_summary():
    records = [
        {"round": 1, "accuracy": 0.40, "loss": 1.5},
        {"round": 2, "accuracy": 0.55, "loss": 1.1},
        {"round": 3, "accuracy": 0.60, "loss": 0.9},
        {"round": 4, "accuracy": 0.58, "loss": 0.8},
    ]

    summary = compute_summary(records)

    assert summary["rounds"] == 4
    assert summary["final_accuracy"] == 0.58
    assert summary["best_accuracy"] == 0.60
    assert summary["best_round"] == 3

    expected_avg = (0.55 + 0.60 + 0.58) / 3
    assert abs(summary["avg_last_3_accuracy"] - expected_avg) < 1e-8


def test_empty_records():
    assert compute_summary([]) is None