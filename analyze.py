import sys

from fl_analyzer.parser import parse_log


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <log_file>")
        return

    log_file = sys.argv[1]
    records = parse_log(log_file)

    if not records:
        print("No valid experiment records found.")
        return

    final_accuracy = records[-1]["accuracy"]
    best_record = max(records, key=lambda x: x["accuracy"])

    print(f"Rounds: {len(records)}")
    print(f"Final Accuracy: {final_accuracy:.4f}")
    print(f"Best Accuracy: {best_record['accuracy']:.4f}")
    print(f"Best Round: {best_record['round']}")


if __name__ == "__main__":
    main()