import heapq
import math
from itertools import count

from order import Order


class MatchingEngine:
    def __init__(self):
        # Separate order books for each trading symbol
        self._buy_heaps = {}
        self._sell_heaps = {}

        self.trades = []
        self.order_ids = set()
        self._sequence = count()

    def _get_heaps(self, symbol):
        if symbol not in self._buy_heaps:
            self._buy_heaps[symbol] = []
            self._sell_heaps[symbol] = []

        return self._buy_heaps[symbol], self._sell_heaps[symbol]

    @property
    def buy_orders(self):
        """All BUY orders, sorted by price and FIFO priority."""
        return [
            entry[2]
            for symbol in self._buy_heaps
            for entry in sorted(self._buy_heaps[symbol])
        ]

    @property
    def sell_orders(self):
        """All SELL orders, sorted by price and FIFO priority."""
        return [
            entry[2]
            for symbol in self._sell_heaps
            for entry in sorted(self._sell_heaps[symbol])
        ]

    def add_order(self, order: Order):
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

        if not isinstance(order.symbol, str) or not order.symbol.strip():
            raise ValueError("Symbol must be a non-empty string")

        symbol = order.symbol.strip().upper()
        order.symbol = symbol

        buy_heap, sell_heap = self._get_heaps(symbol)
        sequence_number = next(self._sequence)

        if order.side == "BUY":
            heapq.heappush(
                buy_heap,
                (-order.price, sequence_number, order)
            )
        else:
            heapq.heappush(
                sell_heap,
                (order.price, sequence_number, order)
            )

        self.order_ids.add(order.order_id)

    def match_orders(self):
        """Match orders only when their trading symbols are identical."""
        for symbol in self._buy_heaps:
            buy_heap = self._buy_heaps[symbol]
            sell_heap = self._sell_heaps[symbol]

            while buy_heap and sell_heap:
                buy_entry = buy_heap[0]
                sell_entry = sell_heap[0]

                buy = buy_entry[2]
                sell = sell_entry[2]

                if buy.price < sell.price:
                    break

                traded_quantity = min(buy.quantity, sell.quantity)
                trade_price = sell.price

                self.trades.append({
                    "buy_order_id": buy.order_id,
                    "sell_order_id": sell.order_id,
                    "symbol": symbol,
                    "price": trade_price,
                    "quantity": traded_quantity
                })

                buy.quantity -= traded_quantity
                sell.quantity -= traded_quantity

                if buy.quantity == 0:
                    heapq.heappop(buy_heap)

                if sell.quantity == 0:
                    heapq.heappop(sell_heap)

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
