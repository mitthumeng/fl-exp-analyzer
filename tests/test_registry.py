import json

from fl_analyzer.registry import load_run, list_runs


def test_load_run(tmp_path):
    run_dir = tmp_path / "run-001"
    run_dir.mkdir()

    manifest = {
        "experiment": {
            "dataset": "MNIST",
            "aggregation": "FedAvg",
            "attack": "LabelFlipping",
            "seed": 117,
        }
    }

    status = {
        "status": "completed",
        "started_at": "2026-09-25T10:00:00+00:00",
        "finished_at": "2026-09-25T10:10:00+00:00",
        "return_code": 0,
    }

    (run_dir / "manifest.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    (run_dir / "status.json").write_text(
        json.dumps(status),
        encoding="utf-8",
    )

    run = load_run(run_dir)

    assert run["run_id"] == "run-001"
    assert run["dataset"] == "MNIST"
    assert run["aggregation"] == "FedAvg"
    assert run["attack"] == "LabelFlipping"
    assert run["seed"] == 117
    assert run["status"] == "completed"
    assert run["return_code"] == 0


def test_run_without_status(tmp_path):
    run_dir = tmp_path / "run-002"
    run_dir.mkdir()

    manifest = {
        "experiment": {
            "dataset": "CIFAR10",
            "aggregation": "Median",
            "attack": "GradientAscent",
            "seed": 1,
        }
    }

    (run_dir / "manifest.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    run = load_run(run_dir)

    assert run["status"] == "unknown"
    assert run["return_code"] is None


def test_list_runs(tmp_path):
    for name in ["run-001", "run-002"]:
        run_dir = tmp_path / name
        run_dir.mkdir()

        manifest = {
            "experiment": {
                "dataset": "MNIST",
                "aggregation": "FedAvg",
                "attack": "none",
                "seed": 1,
            }
        }

        (run_dir / "manifest.json").write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

    runs = list_runs(tmp_path)

    assert len(runs) == 2


def test_list_runs_missing_directory(tmp_path):
    runs = list_runs(tmp_path / "missing")

    assert runs == []