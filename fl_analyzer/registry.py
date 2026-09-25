import json
from pathlib import Path


def load_run(run_dir):
    run_dir = Path(run_dir)

    manifest_path = run_dir / "manifest.json"
    status_path = run_dir / "status.json"

    if not manifest_path.exists():
        return None

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    status = {}

    if status_path.exists():
        with status_path.open("r", encoding="utf-8") as f:
            status = json.load(f)

    experiment = manifest.get("experiment", {})

    return {
        "run_id": run_dir.name,
        "dataset": experiment.get("dataset", "Unknown"),
        "aggregation": experiment.get("aggregation", "Unknown"),
        "attack": experiment.get("attack", "Unknown"),
        "seed": experiment.get("seed", "Unknown"),
        "status": status.get("status", "unknown"),
        "started_at": status.get("started_at"),
        "finished_at": status.get("finished_at"),
        "return_code": status.get("return_code"),
        "path": str(run_dir),
    }


def list_runs(base_dir="runs"):
    base_path = Path(base_dir)

    if not base_path.exists():
        return []

    runs = []

    for run_dir in sorted(base_path.iterdir(), reverse=True):
        if not run_dir.is_dir():
            continue

        run = load_run(run_dir)

        if run is not None:
            runs.append(run)

    return runs