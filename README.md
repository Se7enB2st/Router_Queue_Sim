# Router Queue Simulator
TELCOM 2310 - Project 1

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
