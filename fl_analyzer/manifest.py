import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from fl_analyzer.config import ExperimentConfig


def get_git_commit():
    try:
        result = subprocess.run(
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_git_dirty():
    try:
        result = subprocess.run(
            [
                "git",
                "status",
                "--porcelain",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return bool(result.stdout.strip())

    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def build_manifest(config: ExperimentConfig):
    return {
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "experiment": config.to_dict(),
        "code": {
            "git_commit": get_git_commit(),
            "git_dirty": get_git_dirty(),
        },
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "python_executable": sys.executable,
        },
    }


def save_manifest(
    config: ExperimentConfig,
    output_path,
):
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = build_manifest(config)

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            manifest,
            f,
            indent=2,
            ensure_ascii=False,
        )

    return manifest