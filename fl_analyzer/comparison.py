import csv
import os


def export_comparison(results, output_path="results/comparison.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "experiment",
            "rounds",
            "final_accuracy",
            "best_accuracy",
            "best_round",
            "avg_last_3_accuracy",
        ])

        for result in results:
            writer.writerow([
                result["name"],
                result["rounds"],
                result["final_accuracy"],
                result["best_accuracy"],
                result["best_round"],
                result["avg_last_3_accuracy"],
            ])