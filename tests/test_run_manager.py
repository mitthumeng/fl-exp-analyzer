from datetime import datetime

import pytest

from fl_analyzer.config import ExperimentConfig
from fl_analyzer.run_manager import (
    build_run_id,
    create_run_directory,
)


def make_config():
    return ExperimentConfig(
        dataset="MNIST",
        aggregation="FedAvg",
        attack="LabelFlipping",
        seed=117,
    )


def test_build_run_id():
    config = make_config()

    timestamp = datetime(
        2026,
        9,
        25,
        21,
        45,
        12,
        123456,
    )

    run_id = build_run_id(
        config,
        timestamp=timestamp,
    )

    assert run_id == (
        "20260925-214512-123456_mnist_fedavg_seed117"
    )


def test_create_run_directory(tmp_path):
    config = make_config()

    run_dir = create_run_directory(
        config,
        base_dir=tmp_path,
        run_id="test-run",
    )

    assert run_dir.exists()
    assert (run_dir / "artifacts").is_dir()
    assert (run_dir / "config.yaml").exists()
    assert (run_dir / "manifest.json").exists()


def test_duplicate_run_directory_fails(tmp_path):
    config = make_config()

    create_run_directory(
        config,
        base_dir=tmp_path,
        run_id="duplicate-run",
    )

    with pytest.raises(FileExistsError):
        create_run_directory(
            config,
            base_dir=tmp_path,
            run_id="duplicate-run",
        )