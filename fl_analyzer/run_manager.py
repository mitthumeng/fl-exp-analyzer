import re
from datetime import datetime
from pathlib import Path

import yaml

from fl_analyzer.config import ExperimentConfig
from fl_analyzer.manifest import save_manifest


def _slugify(value):
    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def build_run_id(config: ExperimentConfig, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()

    time_part = timestamp.strftime(
        "%Y%m%d-%H%M%S-%f"
    )

    parts = [
        time_part,
        _slugify(config.dataset),
        _slugify(config.aggregation),
        f"seed{config.seed}",
    ]

    return "_".join(parts)


def create_run_directory(
    config: ExperimentConfig,
    base_dir="runs",
    run_id=None,
):
    base_path = Path(base_dir)

    if run_id is None:
        run_id = build_run_id(config)

    run_dir = base_path / run_id

    if run_dir.exists():
        raise FileExistsError(
            f"Run directory already exists: {run_dir}"
        )

    run_dir.mkdir(parents=True)

    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir()

    config_path = run_dir / "config.yaml"

    with config_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            config.to_dict(),
            f,
            sort_keys=False,
        )

    manifest_path = run_dir / "manifest.json"

    save_manifest(
        config,
        manifest_path,
    )

    return run_dir