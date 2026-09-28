from dataclasses import dataclass
from pathlib import Path

from fl_analyzer.retry import retry_run


@dataclass
class RetryPolicy:
    max_retries: int = 3

    def validate(self):
        if self.max_retries < 0:
            raise ValueError(
                "max_retries must be non-negative"
            )


def retry_with_policy(
    run_dir,
    policy: RetryPolicy,
    base_dir="runs",
):
    policy.validate()

    current_run = Path(run_dir)

    attempts = []

    for attempt_number in range(
        1,
        policy.max_retries + 1,
    ):
        new_run_dir, status = retry_run(
            current_run,
            base_dir=base_dir,
        )

        attempt = {
            "attempt": attempt_number,
            "source_run": current_run.name,
            "new_run": new_run_dir.name,
            "status": status["status"],
            "return_code": status["return_code"],
        }

        attempts.append(attempt)

        if status["status"] == "completed":
            return {
                "status": "completed",
                "attempts": attempts,
                "final_run": str(new_run_dir),
            }

        current_run = new_run_dir

    return {
        "status": "failed",
        "attempts": attempts,
        "final_run": (
            str(current_run)
            if attempts
            else str(run_dir)
        ),
    }