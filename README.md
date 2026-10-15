
# ChronosMatch
### Python-Based Order Matching Engine for Simulated Trading

ChronosMatch is a Python project that simulates a basic trading order book. It matches buy and sell orders according to price priority and order arrival time.

## Features

- Buy and sell order management
- Price-based order priority
- FIFO (First In, First Out) for orders at the same price
- Automatic matching of compatible buy and sell orders
- Partial order execution
- Duplicate order ID validation
- Unit testing with Python's unittest framework
- Basic performance benchmarking

## Project Structure

```text
ChronosMatch/
├── order.py
├── matching_engine.py
├── test_engine.py
├── benchmark.py
├── benchmark_results.md
└── README.md
```

## Requirements

- Python 3.10 or later recommended
- No third-party packages required for the core engine and tests

## How to Run

Run the matching engine:

```bash
python matching_engine.py
```

## Run Unit Tests

```bash
python -m unittest test_engine -v
```

## Run Benchmark

```bash
python benchmark.py
```

The benchmark measures order matching time for the configured workload. Results may vary between runs and depend on the machine and workload.

## Scope

This project focuses on the core order matching engine. It is an educational simulation and is not a production-ready high-frequency trading system.

## Current Status

- Core matching logic implemented
- Order validation implemented
- Unit tests passing
- Basic benchmark implemented
- Documentation in progress
