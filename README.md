# FL Experiment Analyzer

A lightweight Python toolkit for analyzing and comparing federated learning experiment logs.

The project supports single-experiment analysis, multi-experiment comparison, experiment metadata parsing, grouped statistical summaries, visualization, CSV export, and automated tests.

## Features

- Parse federated learning experiment logs
- Extract round-level metrics:
  - Accuracy
  - Loss
- Parse experiment metadata:
  - Dataset
  - Aggregation method
  - Attack
  - Seed
- Compute summary metrics:
  - Final accuracy
  - Best accuracy
  - Best-performing round
  - Average accuracy over the last three rounds
- Generate:
  - Accuracy curves
  - Loss curves
- Compare multiple experiments
- Automatically scan directories for `.log` files
- Compute grouped statistics with mean and standard deviation
- Group experiments by:
  - Aggregation
  - Attack
  - Dataset + Aggregation
  - Dataset + Attack + Aggregation
  - Custom combinations through `--group-by`
- Export summaries to CSV
- Run automated tests with `pytest`

## Project Structure

```text
fl-exp-analyzer/
├── README.md
├── requirements.txt
├── pytest.ini
├── analyze.py
├── compare.py
├── fl_analyzer/
│   ├── __init__.py
│   ├── parser.py
│   ├── metrics.py
│   ├── visualization.py
│   ├── exporter.py
│   ├── comparison.py
│   └── grouping.py
├── sample_logs/
│   ├── example.log
│   ├── experiment_a.log
│   └── experiment_b.log
└── tests/
    ├── test_parser.py
    ├── test_metrics.py
    ├── test_compare.py
    ├── test_metadata.py
    ├── test_grouping.py
    ├── test_dataset_grouping.py
    └── test_dataset_attack_grouping.py