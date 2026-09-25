# Experiment Configuration and Reproducibility Manifest

## Problem

Experiment parameters are currently encoded primarily in log files
and command-line invocations. This makes it difficult to reconstruct
the exact configuration used for an earlier federated learning run.

## Current Limitation

The analyzer can parse experiment results after execution, but it does
not have a canonical representation of experiment configuration and
does not record the source-code or runtime environment associated with
a result.

## Design

Introduce a typed `ExperimentConfig` object loaded from YAML.

The initial schema records:

- dataset
- aggregation
- attack
- seed
- rounds
- local epochs
- batch size
- learning rate
- number of clients
- malicious-client ratio

Each run can additionally generate a JSON reproducibility manifest
containing the experiment configuration, current Git commit, dirty
working-tree state, Python version, executable, platform, and creation
time.

## Alternatives Considered

### Store configuration only inside logs

This requires custom parsing and makes configuration harder to validate
before execution.

### Use JSON configuration

JSON is simple to parse but less convenient for manually maintained
experiment configurations.

### Use YAML configuration

YAML provides a human-readable experiment definition while allowing
the configuration to be parsed into a validated internal schema.

## Validation

The feature is validated through unit tests covering:

- valid YAML configuration loading
- invalid experiment parameters
- missing configuration files
- manifest generation
- manifest persistence

## Future Work

The configuration schema will later be used by the experiment runner,
batch execution system, and result tracking subsystem.