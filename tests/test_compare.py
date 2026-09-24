from pathlib import Path

from compare import collect_log_files


def test_collect_log_files_from_directory(tmp_path):
    log_a = tmp_path / "a.log"
    log_b = tmp_path / "b.log"
    txt_file = tmp_path / "notes.txt"

    log_a.write_text("test", encoding="utf-8")
    log_b.write_text("test", encoding="utf-8")
    txt_file.write_text("ignore", encoding="utf-8")

    files = collect_log_files([str(tmp_path)])

    names = [path.name for path in files]

    assert names == ["a.log", "b.log"]


def test_collect_log_files_from_explicit_files(tmp_path):
    log_a = tmp_path / "a.log"
    log_b = tmp_path / "b.log"

    log_a.write_text("test", encoding="utf-8")
    log_b.write_text("test", encoding="utf-8")

    files = collect_log_files([
        str(log_a),
        str(log_b),
    ])

    assert files == [
        Path(log_a),
        Path(log_b),
    ]


def test_collect_log_files_mixed_input(tmp_path):
    log_a = tmp_path / "a.log"
    subdir = tmp_path / "logs"
    subdir.mkdir()

    log_b = subdir / "b.log"
    log_c = subdir / "c.log"

    log_a.write_text("test", encoding="utf-8")
    log_b.write_text("test", encoding="utf-8")
    log_c.write_text("test", encoding="utf-8")

    files = collect_log_files([
        str(log_a),
        str(subdir),
    ])

    names = [path.name for path in files]

    assert names == ["a.log", "b.log", "c.log"]