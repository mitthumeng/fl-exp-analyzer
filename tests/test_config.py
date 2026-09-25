import pytest

from fl_analyzer.config import (
    ExperimentConfig,
    load_config,
)


def test_load_valid_config(tmp_path):
    config_file = tmp_path / "experiment.yaml"

    config_file.write_text(
        """
dataset: MNIST
aggregation: FedAvg
attack: LabelFlipping
seed: 117
rounds: 100
clients: 20
malicious_ratio: 0.3
""",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config.dataset == "MNIST"
    assert config.aggregation == "FedAvg"
    assert config.attack == "LabelFlipping"
    assert config.seed == 117
    assert config.rounds == 100
    assert config.clients == 20


def test_invalid_malicious_ratio():
    config = ExperimentConfig(
        dataset="MNIST",
        aggregation="FedAvg",
        attack="LabelFlipping",
        seed=117,
        malicious_ratio=1.5,
    )

    with pytest.raises(ValueError):
        config.validate()


def test_invalid_rounds():
    config = ExperimentConfig(
        dataset="MNIST",
        aggregation="FedAvg",
        attack="LabelFlipping",
        seed=117,
        rounds=0,
    )

    with pytest.raises(ValueError):
        config.validate()


def test_missing_config_file():
    with pytest.raises(FileNotFoundError):
        load_config("does_not_exist.yaml")