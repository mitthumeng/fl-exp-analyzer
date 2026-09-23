import csv
import os


def export_summary(summary, output_path="results/summary.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "rounds",
            "final_accuracy",
            "best_accuracy",
            "best_round",
            "avg_last_3_accuracy",
        ])

        writer.writerow([
            summary["rounds"],
            summary["final_accuracy"],
            summary["best_accuracy"],
            summary["best_round"],
            summary["avg_last_3_accuracy"],
        ])