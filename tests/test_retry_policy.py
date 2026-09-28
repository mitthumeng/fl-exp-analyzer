import json
import sys

import pytest
import yaml

from fl_analyzer.retry_policy import (
    RetryPolicy,
    retry_with_policy,
)


def create_failed_run(
    tmp_path,
    command,
    name="failed-run",
):
    run_dir = tmp_path / name
    run_dir.mkdir()

    config = {
        "dataset": "MNIST",
        "aggregation": "FedAvg",
        "attack": "LabelFlipping",
        "seed": 117,
    }

    with (
        run_dir / "config.yaml"
    ).open(
        "w",
        encoding="utf-8",
    ) as f:
        yaml.safe_dump(
            config,
            f,
        )

    status = {
        "status": "failed",
        "return_code": 1,
        "command": command,
    }

    (
        run_dir / "status.json"
    ).write_text(
        json.dumps(status),
        encoding="utf-8",
    )

    return run_dir


def test_retry_policy_success(tmp_path):
    command = [
        sys.executable,
        "-c",
        "print('retry success')",
    ]

    failed_run = create_failed_run(
        tmp_path,
        command,
    )

    policy = RetryPolicy(
        max_retries=3
    )

    result = retry_with_policy(
        failed_run,
        policy,
        base_dir=tmp_path / "retries",
    )

    assert result["status"] == "completed"
    assert len(result["attempts"]) == 1
    assert (
        result["attempts"][0]["return_code"]
        == 0
    )


def test_retry_policy_exhausted(tmp_path):
    command = [
        sys.executable,
        "-c",
        (
            "import sys; "
            "print('still failing'); "
            "sys.exit(2)"
        ),
    ]

    failed_run = create_failed_run(
        tmp_path,
        command,
    )

    policy = RetryPolicy(
        max_retries=2
    )

    result = retry_with_policy(
        failed_run,
        policy,
        base_dir=tmp_path / "retries",
    )

    assert result["status"] == "failed"
    assert len(result["attempts"]) == 2

    assert all(
        attempt["return_code"] == 2
        for attempt in result["attempts"]
    )


def test_zero_retry_policy(tmp_path):
    command = [
        sys.executable,
        "-c",
        "print('unused')",
    ]

    failed_run = create_failed_run(
        tmp_path,
        command,
    )

    policy = RetryPolicy(
        max_retries=0
    )

    result = retry_with_policy(
        failed_run,
        policy,
        base_dir=tmp_path / "retries",
    )

    assert result["status"] == "failed"
    assert result["attempts"] == []


def test_invalid_retry_policy():
    policy = RetryPolicy(
        max_retries=-1
    )

    with pytest.raises(ValueError):
        policy.validate()