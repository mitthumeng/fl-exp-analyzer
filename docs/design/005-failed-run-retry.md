# Failed Run Retry

## Problem

Failed experiment runs are preserved in the registry, but recovering
from a failure currently requires manually reconstructing the original
configuration and execution command.

## Design

A failed run can be retried using its existing:

- `config.yaml`
- `status.json`
- original execution command

The retry creates a new run rather than modifying the failed run.

The new run stores `retry.json`, linking it to the original failed run.

## External Behavior

Users can run:

`python retry_run.py <failed-run-directory>`

Only runs whose status is `failed` may be retried.

## Validation

Tests verify:

- successful retry of a failed run;
- preservation of the original run;
- creation of retry lineage metadata;
- rejection of retries for completed runs.

## Future Work

Retry policies will later support retry limits, automatic retries,
failure classification, and resume-from-checkpoint behavior.