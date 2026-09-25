import json

from fl_analyzer.config import ExperimentConfig
from fl_analyzer.manifest import (
    build_manifest,
    save_manifest,
)


def test_build_manifest():
    config = ExperimentConfig(
        dataset="MNIST",
        aggregation="FedAvg",
        attack="LabelFlipping",
        seed=117,
    )

    manifest = build_manifest(config)

    assert "created_at" in manifest
    assert "experiment" in manifest
    assert "code" in manifest
    assert "environment" in manifest

    assert (
        manifest["experiment"]["dataset"]
        == "MNIST"
    )

    assert (
        manifest["experiment"]["seed"]
        == 117
    )


def test_save_manifest(tmp_path):
    config = ExperimentConfig(
        dataset="CIFAR10",
        aggregation="Median",
        attack="GradientAscent",
        seed=1,
    )

    output = (
        tmp_path
        / "run"
        / "manifest.json"
    )

    save_manifest(
        config,
        output,
    )

    assert output.exists()

    data = json.loads(
        output.read_text(
            encoding="utf-8"
        )
    )

    assert (
        data["experiment"]["dataset"]
        == "CIFAR10"
    )

    assert (
        data["experiment"]["aggregation"]
        == "Median"
    )
    