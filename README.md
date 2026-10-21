
# ChronosMatch

### Python-Based Order Matching Engine for Simulated Trading

ChronosMatch is a Python-based simulated trading engine that matches buy and sell orders using price-time priority. It uses heap-based data structures to efficiently select the highest-priority orders.

## Features

- Buy and sell order management
- Price-time priority matching
- FIFO (First In, First Out) for orders at the same price
- Heap-based order prioritization
- Automatic matching of compatible orders
- Partial order execution
- Order validation and duplicate ID protection
- Unit testing with Python's `unittest` framework
- Performance benchmarking for different workloads

## Project Structure

```text
ChronosMatch/
├── .gitignore
├── README.md
├── order.py
├── matching_engine.py
├── test_engine.py
├── benchmark.py
└── benchmark_results.md
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

The tests cover order validation, price priority, FIFO behavior, partial fills, and other matching scenarios.

## Run Benchmarks

```bash
python benchmark.py
```

Benchmark results and methodology are documented in `benchmark_results.md`. Performance can vary depending on the machine and workload.

## Matching Rules

- Buy orders with higher prices receive priority.
- Sell orders with lower prices receive priority.
- Orders at the same price are processed in arrival order.
- A trade occurs when the best buy price meets or exceeds the best sell price.
- Partially filled orders remain in the order book until completed.

## Scope and Limitations

ChronosMatch is an educational simulation focused on the core order matching engine. It is not a production-ready high-frequency trading system and does not implement a real exchange connection, live market data, or production trading infrastructure.

## Project Status

- Core matching engine implemented using heaps
- Order validation implemented
- Unit tests implemented
- Benchmark script and results documented
- Team-level integration and additional project documentation may still be in progress
