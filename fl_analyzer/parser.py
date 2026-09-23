import re


def parse_log(file_path):
    records = []

    pattern = re.compile(
        r"Round\s+(\d+)\s+\|\s+Accuracy:\s+([0-9.]+)\s+\|\s+Loss:\s+([0-9.]+)"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)

            if match:
                records.append(
                    {
                        "round": int(match.group(1)),
                        "accuracy": float(match.group(2)),
                        "loss": float(match.group(3)),
                    }
                )

    return records