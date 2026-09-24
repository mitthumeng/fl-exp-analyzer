import os
import re


LOG_PATTERN = re.compile(
    r"Round\s+(\d+)\s*\|\s*Accuracy:\s*([0-9]*\.?[0-9]+)"
    r"\s*\|\s*Loss:\s*([0-9]*\.?[0-9]+)"
)


def parse_log(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Log file not found: {file_path}")

    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")

    records = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            match = LOG_PATTERN.search(line)

            if not match:
                continue

            round_id = int(match.group(1))
            accuracy = float(match.group(2))
            loss = float(match.group(3))

            if not 0.0 <= accuracy <= 1.0:
                continue

            if loss < 0:
                continue

            records.append(
                {
                    "round": round_id,
                    "accuracy": accuracy,
                    "loss": loss,
                }
            )

    return records