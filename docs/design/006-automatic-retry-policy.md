# Automatic Retry Policy

## Problem

The platform supports manually retrying a failed experiment, but repeated
failures still require the user to invoke the retry command manually.

For long-running federated learning workloads, temporary failures such as
resource interruptions should not require repeated manual intervention.

## Design

Introduce a configurable retry policy with a maximum number of retry
attempts.

Each retry creates a new managed run and therefore preserves:

- the original failed run;
- its configuration;
- its logs;
- its status;
- retry lineage.

The retry loop stops immediately when an experiment completes successfully.

## External Behavior

A failed run can be retried automatically with:

```bash
python auto_retry_run.py \
    runs/<failed-run> \
    --max-retries 3