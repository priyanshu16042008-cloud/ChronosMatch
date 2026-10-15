
import time
from order import Order
from matching_engine import MatchingEngine


def benchmark_matching(total_orders=1000):
    engine = MatchingEngine()

    # Add buy orders
    for i in range(1, total_orders + 1):
        engine.add_order(Order(i, "BUY", 100.0, 1))

    # Add sell orders
    for i in range(total_orders + 1, 2 * total_orders + 1):
        engine.add_order(Order(i, "SELL", 100.0, 1))

    start_time = time.perf_counter()
    engine.match_orders()
    elapsed = time.perf_counter() - start_time

    print(f"Buy orders: {total_orders}")
    print(f"Sell orders: {total_orders}")
    print(f"Trades executed: {len(engine.trades)}")
    print(f"Matching time: {elapsed:.6f} seconds")

    if elapsed > 0:
        print(f"Trades per second: {len(engine.trades) / elapsed:.2f}")


if __name__ == "__main__":
    benchmark_matching()