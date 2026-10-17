
# ChronosMatch Benchmark Results

## Baseline - Initial Recorded Run

- Buy Orders: 1000
- Sell Orders: 1000
- Trades Executed: 1000
- Matching Time: 0.000997 seconds
- Throughput: 1,003,210.27 trades/second

## Additional Run

- Buy Orders: 1000
- Sell Orders: 1000
- Trades Executed: 1000
- Matching Time: 0.000435 seconds
- Throughput: 2,296,738.63 trades/second

## Notes

- Benchmark ran locally using Python.
- Results vary between runs and depend on system conditions.
- The benchmark measures matching time only; order insertion time is excluded.
- These are preliminary measurements, not proof of production HFT performance.
- Repeated trials and larger workloads are needed for a more reliable comparison.
## Heap-Based Engine Benchmark

Latest benchmark run with the optimized heap-based matching engine.

| Orders per Side | Trades Executed | Insertion Time (s) | Matching Time (s) | Total Time (s) | Throughput (orders/s) |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 1,000 | 0.001662 | 0.001064 | 0.002726 | 733,794.16 |
| 5,000 | 5,000 | 0.013542 | 0.015106 | 0.028648 | 349,064.02 |
| 10,000 | 10,000 | 0.021702 | 0.015537 | 0.037239 | 537,074.23 |

### Notes

- The optimized engine uses heaps for price priority.
- The benchmark includes order insertion and matching time.
- Each workload was measured using the benchmark script's repeated trials.
- Results may vary depending on machine load and system conditions.
- These results are local measurements, not proof of production HFT performance.
- The latest results are not directly comparable with the original baseline because the measurement methodology and workload differ.
