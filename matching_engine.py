
import heapq
import math
from itertools import count

from order import Order


class MatchingEngine:
    def __init__(self):
        # BUY: highest price first, then earlier order first
        self._buy_heap = []

        # SELL: lowest price first, then earlier order first
        self._sell_heap = []

        self.trades = []
        self.order_ids = set()
        self._sequence = count()

    @property
    def buy_orders(self):
        """Return BUY orders in price-priority and FIFO order."""
        return [
            entry[2]
            for entry in sorted(self._buy_heap)
        ]

    @property
    def sell_orders(self):
        """Return SELL orders in price-priority and FIFO order."""
        return [
            entry[2]
            for entry in sorted(self._sell_heap)
        ]

    def add_order(self, order: Order):
        # Validate before reserving the order ID.
        if order.order_id in self.order_ids:
            raise ValueError("Duplicate order ID")

        if order.side not in ("BUY", "SELL"):
            raise ValueError("Invalid order side")

        if (
            type(order.price) not in (int, float)
            or not math.isfinite(order.price)
            or order.price <= 0
        ):
            raise ValueError("Price must be finite and positive")

        if type(order.quantity) is not int or order.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        sequence_number = next(self._sequence)

        if order.side == "BUY":
            heapq.heappush(
                self._buy_heap,
                (-order.price, sequence_number, order)
            )
        else:
            heapq.heappush(
                self._sell_heap,
                (order.price, sequence_number, order)
            )

        self.order_ids.add(order.order_id)

    def match_orders(self):
        while self._buy_heap and self._sell_heap:
            buy_entry = self._buy_heap[0]
            sell_entry = self._sell_heap[0]

            buy = buy_entry[2]
            sell = sell_entry[2]

            # Stop if the best BUY cannot meet the best SELL.
            if buy.price < sell.price:
                break

            traded_quantity = min(buy.quantity, sell.quantity)
            trade_price = sell.price

            self.trades.append({
                "buy_order_id": buy.order_id,
                "sell_order_id": sell.order_id,
                "price": trade_price,
                "quantity": traded_quantity
            })

            buy.quantity -= traded_quantity
            sell.quantity -= traded_quantity

            if buy.quantity == 0:
                heapq.heappop(self._buy_heap)

            if sell.quantity == 0:
                heapq.heappop(self._sell_heap)

    def show_state(self):
        print("Buy orders:", self.buy_orders)
        print("Sell orders:", self.sell_orders)
        print("Trades:", self.trades)


if __name__ == "__main__":
    engine = MatchingEngine()

    engine.add_order(Order(1, "BUY", 100.0, 10))
    engine.add_order(Order(2, "SELL", 95.0, 6))

    engine.match_orders()
    engine.show_state()
