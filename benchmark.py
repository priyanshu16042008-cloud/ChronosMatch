
import time
from order import Order
#from matching_engine import MatchingEngine
from matching_engine_list import MatchingEngine

def benchmark_matching(total_orders=1000, repeats=5):
    insertion_times = []
    matching_times = []

    for _ in range(repeats):
        engine = MatchingEngine()

        start_insert = time.perf_counter()

        for i in range(1, total_orders + 1):
            engine.add_order(Order(i, "BUY", 100.0, 1))

        for i in range(total_orders + 1, 2 * total_orders + 1):
            engine.add_order(Order(i, "SELL", 100.0, 1))

        insertion_times.append(time.perf_counter() - start_insert)

        start_match = time.perf_counter()
        engine.match_orders()
        matching_times.append(time.perf_counter() - start_match)

        assert len(engine.trades) == total_orders, (
            f"Expected {total_orders} trades, got {len(engine.trades)}"
        )

    avg_insert = sum(insertion_times) / repeats
    avg_match = sum(matching_times) / repeats

    print(f"\nOrders per side: {total_orders}")
    print(f"Trades executed: {total_orders}")
    print(f"Average insertion time: {avg_insert:.6f} seconds")
    print(f"Average matching time: {avg_match:.6f} seconds")
    print(f"Average total time: {avg_insert + avg_match:.6f} seconds")

    if avg_insert + avg_match > 0:
        print(
            "Overall throughput: "
            f"{(2 * total_orders) / (avg_insert + avg_match):.2f} orders/second"
        )


if __name__ == "__main__":
    for size in (1000, 5000, 10000):
        benchmark_matching(total_orders=size)
