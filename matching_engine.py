from order import Order


class MatchingEngine:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trades = []
        self.order_ids = set()

    def add_order(self, order: Order):
        if order.order_id in self.order_ids:
            raise ValueError("Duplicate order ID")

        if order.price <= 0 or order.quantity <= 0:
           raise ValueError("Price and quantity must be positive")
    
        if order.side not in ("BUY", "SELL"):
            raise ValueError("Invalid order side")

        if order.price != order.price or order.price == float("inf") or order.price == float("-inf"):
            raise ValueError("Price must be finite")

        if order.side == "BUY":
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda o: -o.price)
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda o: o.price)

        self.order_ids.add(order.order_id)

    def match_orders(self):
        while self.buy_orders and self.sell_orders:
            buy = self.buy_orders[0]
            sell = self.sell_orders[0]

            # Best buy price must meet or exceed best sell price
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
                self.buy_orders.pop(0)

            if sell.quantity == 0:
                self.sell_orders.pop(0)

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