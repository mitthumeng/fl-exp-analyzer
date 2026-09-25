# Run Registry

## Problem

Managed experiment runs are stored in separate directories, but there is
currently no unified way to inspect experiment history across multiple
runs.

## Design

Introduce a run registry that scans managed run directories and combines
information from:

- `manifest.json`
- `status.json`

Each registry entry exposes:

- run ID
- dataset
- aggregation method
- attack
- seed
- status
- start and finish time
- return code
- run directory path

A command-line interface provides a tabular view of all managed runs.

## External Behavior

Users can now run:

`python list_runs.py`

to inspect previously created experiments.

Runs created without execution status are reported as `unknown`, while
managed executions can report `running`, `completed`, or `failed`.

## Validation

Tests cover:

- loading a completed run
- loading a run without status information
- discovering multiple runs
- handling a missing runs directory

## Future Work

The registry will later support filtering by dataset, attack,
aggregation, seed, and run status, as well as result extraction and
failure recovery.