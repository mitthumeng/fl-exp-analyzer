import json

from fl_analyzer.registry import (
    compute_retry_counts,
    filter_runs,
    list_runs,
    load_run,
)


def write_manifest(
    run_dir,
    dataset="MNIST",
    aggregation="FedAvg",
    attack="LabelFlipping",
    seed=117,
):
    manifest = {
        "experiment": {
            "dataset": dataset,
            "aggregation": aggregation,
            "attack": attack,
            "seed": seed,
        }
    }

    (run_dir / "manifest.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )


def write_status(
    run_dir,
    status="completed",
    return_code=0,
):
    data = {
        "status": status,
        "started_at": "2026-09-28T10:00:00+00:00",
        "finished_at": "2026-09-28T10:10:00+00:00",
        "return_code": return_code,
    }

    (run_dir / "status.json").write_text(
        json.dumps(data),
        encoding="utf-8",
    )


def test_load_run(tmp_path):
    run_dir = tmp_path / "run-001"
    run_dir.mkdir()

    write_manifest(run_dir)
    write_status(run_dir)

    run = load_run(run_dir)

    assert run["run_id"] == "run-001"
    assert run["dataset"] == "MNIST"
    assert run["aggregation"] == "FedAvg"
    assert run["attack"] == "LabelFlipping"
    assert run["seed"] == 117
    assert run["status"] == "completed"
    assert run["return_code"] == 0
    assert run["retry_of"] is None


def test_run_without_status(tmp_path):
    run_dir = tmp_path / "run-002"
    run_dir.mkdir()

    write_manifest(
        run_dir,
        dataset="CIFAR10",
        aggregation="Median",
        attack="GradientAscent",
        seed=1,
    )

    run = load_run(run_dir)

    assert run["status"] == "unknown"
    assert run["return_code"] is None


def test_load_retry_run(tmp_path):
    run_dir = tmp_path / "retry-run"
    run_dir.mkdir()

    write_manifest(run_dir)
    write_status(run_dir)

    retry_data = {
        "retry_of": "original-run"
    }

    (run_dir / "retry.json").write_text(
        json.dumps(retry_data),
        encoding="utf-8",
    )

    run = load_run(run_dir)

    assert run["retry_of"] == "original-run"


def test_list_runs(tmp_path):
    for name in [
        "run-001",
        "run-002",
    ]:
        run_dir = tmp_path / name
        run_dir.mkdir()

        write_manifest(run_dir)

    runs = list_runs(tmp_path)

    assert len(runs) == 2


def test_list_runs_missing_directory(tmp_path):
    runs = list_runs(
        tmp_path / "missing"
    )

    assert runs == []


def test_filter_runs():
    runs = [
        {
            "dataset": "MNIST",
            "aggregation": "FedAvg",
            "attack": "LabelFlipping",
            "seed": 117,
            "status": "completed",
        },
        {
            "dataset": "CIFAR10",
            "aggregation": "Median",
            "attack": "GradientAscent",
            "seed": 1,
            "status": "failed",
        },
    ]

    filtered = filter_runs(
        runs,
        dataset="MNIST",
        status="completed",
    )

    assert len(filtered) == 1
    assert (
        filtered[0]["aggregation"]
        == "FedAvg"
    )


def test_filter_runs_combined():
    runs = [
        {
            "dataset": "MNIST",
            "aggregation": "FedAvg",
            "attack": "LabelFlipping",
            "seed": 117,
            "status": "completed",
        },
        {
            "dataset": "MNIST",
            "aggregation": "Median",
            "attack": "LabelFlipping",
            "seed": 117,
            "status": "completed",
        },
    ]

    filtered = filter_runs(
        runs,
        dataset="MNIST",
        aggregation="Median",
        attack="LabelFlipping",
        seed=117,
    )

    assert len(filtered) == 1
    assert (
        filtered[0]["aggregation"]
        == "Median"
    )


def test_filter_runs_no_match():
    runs = [
        {
            "dataset": "MNIST",
            "aggregation": "FedAvg",
            "attack": "none",
            "seed": 1,
            "status": "completed",
        }
    ]

    filtered = filter_runs(
        runs,
        status="failed",
    )

    assert filtered == []


def test_compute_retry_counts():
    runs = [
        {
            "run_id": "run-a",
            "retry_of": None,
        },
        {
            "run_id": "run-b",
            "retry_of": "run-a",
        },
        {
            "run_id": "run-c",
            "retry_of": "run-a",
        },
        {
            "run_id": "run-d",
            "retry_of": "run-b",
        },
    ]

    counts = compute_retry_counts(
        runs
    )

    assert counts["run-a"] == 2
    assert counts["run-b"] == 1
    assert "run-c" not in counts