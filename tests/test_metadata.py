import tempfile

from fl_analyzer.parser import parse_metadata


def test_parse_metadata():
    content = """\
Dataset: MNIST
Aggregation: FedAvg
Attack: LabelFlipping
Seed: 117

Round 1 | Accuracy: 0.430 | Loss: 1.75
"""

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".log",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(content)
        path = f.name

    metadata = parse_metadata(path)

    assert metadata["dataset"] == "MNIST"
    assert metadata["aggregation"] == "FedAvg"
    assert metadata["attack"] == "LabelFlipping"
    assert metadata["seed"] == 117


def test_parse_partial_metadata():
    content = """\
Dataset: CIFAR10
Aggregation: Krum

Round 1 | Accuracy: 0.510 | Loss: 1.30
"""

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".log",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(content)
        path = f.name

    metadata = parse_metadata(path)

    assert metadata["dataset"] == "CIFAR10"
    assert metadata["aggregation"] == "Krum"
    assert "attack" not in metadata
    assert "seed" not in metadata