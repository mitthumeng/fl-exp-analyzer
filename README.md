# FL Experiment Analyzer

A lightweight Python tool for analyzing federated learning experiment logs.

The project extracts round-level training metrics from log files, computes summary statistics, generates accuracy and loss curves, and exports experiment summaries to CSV.

## Features

* Parse federated learning training logs
* Extract round number, accuracy, and loss
* Compute experiment summary statistics:

  * Final accuracy
  * Best accuracy
  * Best-performing round
  * Average accuracy over the last three rounds
* Generate accuracy and loss curves
* Export experiment summaries to CSV

## Project Structure

```text
fl-exp-analyzer/
├── README.md
├── requirements.txt
├── analyze.py
├── fl_analyzer/
│   ├── __init__.py
│   ├── parser.py
│   ├── metrics.py
│   ├── visualization.py
│   └── exporter.py
└── sample_logs/
    └── example.log
```

## Installation

It is recommended to use a dedicated Python environment.

Using Conda:

```bash
conda create -n fl-analyzer python=3.12
conda activate fl-analyzer
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the analyzer with a log file:

```bash
python analyze.py sample_logs/example.log
```

Example output:

```text
Rounds: 5
Final Accuracy: 0.6170
Best Accuracy: 0.6230
Best Round: 4
Average Accuracy (Last 3 Rounds): 0.6137
Plots saved to results/
Summary saved to results/summary.csv
```

The generated files are stored in the `results/` directory:

```text
results/
├── accuracy_curve.png
├── loss_curve.png
└── summary.csv
```

## Supported Log Format

The current parser expects log entries in the following format:

```text
Round 1 | Accuracy: 0.412 | Loss: 1.82
Round 2 | Accuracy: 0.535 | Loss: 1.34
Round 3 | Accuracy: 0.601 | Loss: 1.02
```

Each valid line should contain:

* Training round
* Accuracy
* Loss

## Example

A sample log is available at:

```text
sample_logs/example.log
```

You can use it to verify that the project is working correctly:

```bash
python analyze.py sample_logs/example.log
```

## Output

### Summary Metrics

The analyzer reports:

* Total number of parsed rounds
* Final accuracy
* Best accuracy
* Round with the best accuracy
* Average accuracy over the last three rounds

### Visualization

Two plots are generated:

* `accuracy_curve.png`
* `loss_curve.png`

### CSV Export

The experiment summary is exported to:

```text
results/summary.csv
```

## Future Improvements

Possible extensions include:

* Support for multiple log formats
* Comparison of multiple federated learning experiments
* Support for different aggregation methods and attacks
* Configurable output directories
* Command-line argument support
* Automated experiment report generation

## License

This project is intended for educational and research purposes.
