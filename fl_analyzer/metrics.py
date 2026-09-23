def compute_summary(records):
    if not records:
        return None

    final_accuracy = records[-1]["accuracy"]

    best_record = max(
        records,
        key=lambda x: x["accuracy"]
    )

    recent_records = records[-3:]
    avg_last_3 = sum(
        x["accuracy"] for x in recent_records
    ) / len(recent_records)

    return {
        "rounds": len(records),
        "final_accuracy": final_accuracy,
        "best_accuracy": best_record["accuracy"],
        "best_round": best_record["round"],
        "avg_last_3_accuracy": avg_last_3,
    }