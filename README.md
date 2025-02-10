# Router Queue Simulator
##### TELCOM 2310 - Project 1
##### Ethan He (Eth69@pitt.edu)

## Description
This project simulates packet queuing behavior in a router with configurable arrival rates (λ), departure rates (μ), and buffer sizes (n). It consists of two main components:
1. Event simulator (`event_simulator.py`)
2. Results visualizer (`plot_results.py`)

## Requirements
- Python 3.x
- Required Python packages:
  - matplotlib
  - numpy

## Installation
1. Clone or download the project files
2. Install required packages:

```bash
pip install matplotlib numpy
```

## Usage

### 1. Event Simulator
The simulator supports both constant and variable arrival rates.

#### Constant Rate Simulation
```bash
python event_simulator.py -l <lambda> -m <mu> -n <buffer_size> -o <output_file>
```

# Example: λ=30, μ=50, n=50
```bash
python event_simulator.py -l 30 -m 50 -n 50 -o output.txt
```

Parameters:
- `-l, --lambda_rate`: Arrival rate (packets/sec)
- `-m, --mu_rate`: Departure rate (packets/sec)
- `-n, --buffer_size`: Queue buffer size (packets)
- `-x, --num_events`: Number of events (default: 1,000,000)
- `-o, --output_file`: Output file name
- `--debug`: Enable debug output

#### Variable Rate Simulation
```bash
python event_simulator.py -m <mu> -n <buffer_size> --variable_lambda -o <output_file>
```
# Example: μ=120, n=100
```bash
python event_simulator.py -m 120 -n 100 --variable_lambda -o var_output.txt
```

### 2. Results Visualization
```bash
python plot_results.py -i <input_file> -o <output_plot> [options]
```

# Example: Basic plot
```bash
python plot_results.py -i output.txt -o plot.png --normalize
```

# Example: Zoomed view of first 2000 events
```bash
python plot_results.py -i output.txt -o plot.png --normalize --zoom 2000
```

Parameters:
- `-i, --input-file`: Simulator output file
- `-o, --output-file`: Plot output file
- `--normalize`: Normalize data for better visualization
- `--zoom`: Number of events to zoom into
- `--debug`: Show debug information

## Example Scenarios

### 1. Constant Rate Examples

# Scenario 1: λ=30, μ=50, n=50

```bash
python event_simulator.py -l 30 -m 50 -n 50 -o scenario1.txt
python plot_results.py -i scenario1.txt -o plot1.png --normalize
```

# Scenario 2: λ=80, μ=50, n=50

```bash
python event_simulator.py -l 80 -m 50 -n 50 -o scenario2.txt
python plot_results.py -i scenario2.txt -o plot2.png --normalize
```

### 2. Variable Rate Example

# Variable λ with μ=120, n=100

```bash
python event_simulator.py -m 120 -n 100 --variable_lambda -o var_scenario.txt
```

## Output Format
The simulator outputs a text file with three columns:
1. Event number
2. Current queue length
3. Total dropped packets


## Visualization
The plotting script generates:
- Queue length over time (blue dots)
- Cumulative dropped packets (orange dashed line)
- Optional zoomed view for detailed analysis

## Debugging
Add `--debug` flag to either script for detailed output:

```bash
python event_simulator.py -l 80 -m 50 -n 50 -o output.txt --debug
python plot_results.py -i output.txt -o plot.png --normalize --debug
```
