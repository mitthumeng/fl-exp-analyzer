# Failed Run Retry and Retry Lineage

## Problem

Failed experiment runs are preserved by the experiment platform, but
recovering from them manually requires reconstructing the original
configuration and execution command.

Once retries are introduced, another problem appears: experiment history
must preserve the relationship between the failed run and all subsequent
retry attempts.

Without explicit lineage information it becomes difficult to determine
whether two experiment directories represent independent experiments or
different attempts of the same experiment.

## Design

A failed run can be retried using its existing:

- `config.yaml`
- `status.json`
- original execution command

The retry operation never modifies or overwrites the failed run.

Instead, a new managed run is created.

The new run contains a `retry.json` file:

```json
{
  "retry_of": "original-run-id"
}