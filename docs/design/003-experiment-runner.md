# Managed Experiment Runner

## Problem

Experiment configurations and run directories are now structured, but
execution is still manual. There is no consistent mechanism for linking
the exact command, runtime log, exit status, configuration, and
reproducibility metadata for a single experiment.

## Design

Introduce a managed experiment runner that:

1. loads a validated experiment configuration;
2. creates a dedicated run directory;
3. executes the requested command;
4. redirects stdout and stderr to `training.log`;
5. records run state in `status.json`;
6. preserves the exit code and start/finish timestamps.

Run status is represented as:

- `running`
- `completed`
- `failed`

## External Behavior

The new CLI supports:

`python run_experiment.py <config> --command "<command>"`

Each execution produces:

- `config.yaml`
- `manifest.json`
- `training.log`
- `status.json`
- `artifacts/`

## Validation

Tests cover both successful and failed subprocess execution. A failed
experiment must preserve its log and non-zero exit code rather than
silently disappearing.

## Future Work

The next stage will introduce a run registry so that experiment status
and metadata can be queried across multiple run directories.