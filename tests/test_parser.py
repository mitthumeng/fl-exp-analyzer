import tempfile

from fl_analyzer.parser import parse_log


def test_parse_valid_log():
    content = """\
Round 1 | Accuracy: 0.40 | Loss: 1.50
Round 2 | Accuracy: 0.55 | Loss: 1.10
"""

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".log",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(content)
        path = f.name

    records = parse_log(path)

    assert len(records) == 2
    assert records[0]["round"] == 1
    assert records[0]["accuracy"] == 0.40
    assert records[1]["loss"] == 1.10


def test_skip_invalid_lines():
    content = """\
This is not a valid record
Round 1 | Accuracy: 0.45 | Loss: 1.20
Another invalid line
"""

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".log",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(content)
        path = f.name

    records = parse_log(path)

    assert len(records) == 1
    assert records[0]["round"] == 1


def test_skip_invalid_accuracy():
    content = """\
Round 1 | Accuracy: 1.50 | Loss: 1.20
Round 2 | Accuracy: 0.60 | Loss: 0.90
"""

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".log",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(content)
        path = f.name

    records = parse_log(path)

    assert len(records) == 1
    assert records[0]["round"] == 2