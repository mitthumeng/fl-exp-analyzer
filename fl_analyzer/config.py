from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ExperimentConfig:
    dataset: str
    aggregation: str
    attack: str
    seed: int

    rounds: int = 100
    local_epochs: int = 1
    batch_size: int = 64
    learning_rate: float = 0.01

    clients: int = 20
    malicious_ratio: float = 0.0

    def validate(self):
        if not self.dataset:
            raise ValueError("dataset must not be empty")

        if not self.aggregation:
            raise ValueError("aggregation must not be empty")

        if not self.attack:
            raise ValueError("attack must not be empty")

        if self.seed < 0:
            raise ValueError("seed must be non-negative")

        if self.rounds <= 0:
            raise ValueError("rounds must be greater than zero")

        if self.local_epochs <= 0:
            raise ValueError(
                "local_epochs must be greater than zero"
            )

        if self.batch_size <= 0:
            raise ValueError(
                "batch_size must be greater than zero"
            )

        if self.learning_rate <= 0:
            raise ValueError(
                "learning_rate must be greater than zero"
            )

        if self.clients <= 0:
            raise ValueError(
                "clients must be greater than zero"
            )

        if not 0.0 <= self.malicious_ratio <= 1.0:
            raise ValueError(
                "malicious_ratio must be between 0 and 1"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_config(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {file_path}"
        )

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(
            "Configuration file must contain a YAML mapping."
        )

    try:
        config = ExperimentConfig(**data)
    except TypeError as exc:
        raise ValueError(
            f"Invalid experiment configuration: {exc}"
        ) from exc

    config.validate()

    return config