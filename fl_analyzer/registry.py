import json
from pathlib import Path


def load_run(run_dir):
    run_dir = Path(run_dir)

    manifest_path = run_dir / "manifest.json"
    status_path = run_dir / "status.json"
    retry_path = run_dir / "retry.json"

    if not manifest_path.exists():
        return None

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    status = {}

    if status_path.exists():
        with status_path.open("r", encoding="utf-8") as f:
            status = json.load(f)

    retry_info = {}

    if retry_path.exists():
        with retry_path.open("r", encoding="utf-8") as f:
            retry_info = json.load(f)

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
        "retry_of": retry_info.get("retry_of"),
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


def filter_runs(
    runs,
    dataset=None,
    aggregation=None,
    attack=None,
    seed=None,
    status=None,
):
    filtered = []

    for run in runs:
        if dataset is not None and run["dataset"] != dataset:
            continue

        if (
            aggregation is not None
            and run["aggregation"] != aggregation
        ):
            continue

        if attack is not None and run["attack"] != attack:
            continue

        if seed is not None and run["seed"] != seed:
            continue

        if status is not None and run["status"] != status:
            continue

        filtered.append(run)

    return filtered


def compute_retry_counts(runs):
    counts = {}

    for run in runs:
        retry_of = run.get("retry_of")

        if retry_of:
            counts[retry_of] = counts.get(retry_of, 0) + 1

    return counts