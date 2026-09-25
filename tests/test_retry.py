import json
import sys

import pytest
import yaml

from fl_analyzer.retry import retry_run


def create_failed_run(tmp_path):
    run_dir = tmp_path / "failed-run"
    run_dir.mkdir()

    config = {
        "dataset": "MNIST",
        "aggregation": "FedAvg",
        "attack": "LabelFlipping",
        "seed": 117,
    }

    with (run_dir / "config.yaml").open(
        "w",
        encoding="utf-8",
    ) as f:
        yaml.safe_dump(config, f)

    status = {
        "status": "failed",
        "return_code": 1,
        "command": [
            sys.executable,
            "-c",
            "print('retry experiment')",
        ],
    }

    (run_dir / "status.json").write_text(
        json.dumps(status),
        encoding="utf-8",
    )

    return run_dir


def test_retry_failed_run(tmp_path):
    failed_run = create_failed_run(tmp_path)

    new_run_dir, status = retry_run(
        failed_run,
        base_dir=tmp_path / "retries",
    )

    assert new_run_dir.exists()
    assert status["status"] == "completed"
    assert status["return_code"] == 0

    retry_file = new_run_dir / "retry.json"

    assert retry_file.exists()

    retry_data = json.loads(
        retry_file.read_text(encoding="utf-8")
    )

    assert retry_data["retry_of"] == "failed-run"


def test_retry_completed_run_fails(tmp_path):
    run_dir = tmp_path / "completed-run"
    run_dir.mkdir()

    config = {
        "dataset": "MNIST",
        "aggregation": "FedAvg",
        "attack": "none",
        "seed": 1,
    }

    with (run_dir / "config.yaml").open(
        "w",
        encoding="utf-8",
    ) as f:
        yaml.safe_dump(config, f)

    status = {
        "status": "completed",
        "return_code": 0,
        "command": [
            sys.executable,
            "-c",
            "print('done')",
        ],
    }

    (run_dir / "status.json").write_text(
        json.dumps(status),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        retry_run(
            run_dir,
            base_dir=tmp_path / "retries",
        )