import json
import shlex
from pathlib import Path

from fl_analyzer.config import load_config
from fl_analyzer.runner import run_experiment


def load_status(run_dir):
    run_dir = Path(run_dir)
    status_path = run_dir / "status.json"

    if not status_path.exists():
        raise FileNotFoundError(
            f"Status file not found: {status_path}"
        )

    with status_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def retry_run(run_dir, base_dir="runs"):
    run_dir = Path(run_dir)

    config_path = run_dir / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    status = load_status(run_dir)

    if status.get("status") != "failed":
        raise ValueError(
            "Only failed runs can be retried."
        )

    command = status.get("command")

    if not command:
        raise ValueError(
            "Original run does not contain an execution command."
        )

    if isinstance(command, str):
        command = shlex.split(command)

    config = load_config(config_path)

    new_run_dir, new_status = run_experiment(
        config,
        command,
        base_dir=base_dir,
    )

    retry_metadata = {
        "retry_of": run_dir.name,
    }

    retry_path = new_run_dir / "retry.json"

    with retry_path.open("w", encoding="utf-8") as f:
        json.dump(
            retry_metadata,
            f,
            indent=2,
        )

    return new_run_dir, new_status