import sys

from fl_analyzer.config import ExperimentConfig
from fl_analyzer.runner import run_experiment


def make_config():
    return ExperimentConfig(
        dataset="MNIST",
        aggregation="FedAvg",
        attack="LabelFlipping",
        seed=117,
    )


def test_successful_run(tmp_path):
    config = make_config()

    command = [
        sys.executable,
        "-c",
        "print('successful experiment')",
    ]

    run_dir, status = run_experiment(
        config,
        command,
        base_dir=tmp_path,
    )

    assert status["status"] == "completed"
    assert status["return_code"] == 0

    log_path = run_dir / "training.log"
    status_path = run_dir / "status.json"

    assert log_path.exists()
    assert status_path.exists()

    assert "successful experiment" in (
        log_path.read_text(encoding="utf-8")
    )


def test_failed_run(tmp_path):
    config = make_config()

    command = [
        sys.executable,
        "-c",
        "import sys; print('failed experiment'); sys.exit(2)",
    ]

    run_dir, status = run_experiment(
        config,
        command,
        base_dir=tmp_path,
    )

    assert status["status"] == "failed"
    assert status["return_code"] == 2

    log_path = run_dir / "training.log"

    assert "failed experiment" in (
        log_path.read_text(encoding="utf-8")
    )