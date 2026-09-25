import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from fl_analyzer.config import ExperimentConfig
from fl_analyzer.run_manager import create_run_directory


def _now():
    return datetime.now(timezone.utc).isoformat()


def write_status(run_dir, status):
    status_path = Path(run_dir) / "status.json"

    with status_path.open("w", encoding="utf-8") as f:
        json.dump(
            status,
            f,
            indent=2,
            ensure_ascii=False,
        )


def run_experiment(
    config: ExperimentConfig,
    command,
    base_dir="runs",
):
    run_dir = create_run_directory(
        config,
        base_dir=base_dir,
    )

    log_path = run_dir / "training.log"

    status = {
        "status": "running",
        "started_at": _now(),
        "finished_at": None,
        "return_code": None,
        "command": command,
    }

    write_status(run_dir, status)

    try:
        with log_path.open(
            "w",
            encoding="utf-8",
        ) as log_file:
            process = subprocess.run(
                command,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )

        status["return_code"] = process.returncode
        status["finished_at"] = _now()

        if process.returncode == 0:
            status["status"] = "completed"
        else:
            status["status"] = "failed"

    except Exception as exc:
        status["status"] = "failed"
        status["finished_at"] = _now()
        status["error"] = str(exc)

        write_status(run_dir, status)
        raise

    write_status(run_dir, status)

    return run_dir, status