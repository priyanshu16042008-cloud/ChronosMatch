import unittest
from order import Order
from matching_engine import MatchingEngine


class TestMatchingEngine(unittest.TestCase):

    def test_partial_fill(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 100.0, 10))
        engine.add_order(Order(2, "SELL", 95.0, 6))

        engine.match_orders()

        self.assertEqual(len(engine.trades), 1)
        self.assertEqual(engine.trades[0]["quantity"], 6)
        self.assertEqual(engine.buy_orders[0].quantity, 4)
        self.assertEqual(len(engine.sell_orders), 0)

    def test_no_match_when_prices_do_not_cross(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 90.0, 10))
        engine.add_order(Order(2, "SELL", 95.0, 6))

        engine.match_orders()

        self.assertEqual(len(engine.trades), 0)
        self.assertEqual(len(engine.buy_orders), 1)
        self.assertEqual(len(engine.sell_orders), 1)
    def test_higher_buy_price_gets_priority(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 100.0, 5))
        engine.add_order(Order(2, "BUY", 110.0, 5))
        engine.add_order(Order(3, "SELL", 95.0, 5))

        engine.match_orders()

        self.assertEqual(
            engine.trades[0]["buy_order_id"], 2
        )

    def test_lower_sell_price_gets_priority(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "SELL", 100.0, 5))
        engine.add_order(Order(2, "SELL", 90.0, 5))
        engine.add_order(Order(3, "BUY", 110.0, 5))

        engine.match_orders()

        self.assertEqual(
            engine.trades[0]["sell_order_id"], 2
        )
    def test_same_price_earlier_buy_order_gets_priority(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 100.0, 5))
        engine.add_order(Order(2, "BUY", 100.0, 5))
        engine.add_order(Order(3, "SELL", 100.0, 5))

        engine.match_orders()

        self.assertEqual(
            engine.trades[0]["buy_order_id"], 1
        )
    def test_zero_price_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(4, "BUY", 0, 10)

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(5, "SELL", 100, 0)

    def test_same_price_earlier_sell_order_gets_priority(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "SELL", 100.0, 5))
        engine.add_order(Order(2, "SELL", 100.0, 5))
        engine.add_order(Order(3, "BUY", 100.0, 5))

        engine.match_orders()

        self.assertEqual(
            engine.trades[0]["sell_order_id"], 1
        )

    def test_one_buy_order_matches_multiple_sells(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 100.0, 10))
        engine.add_order(Order(2, "SELL", 95.0, 4))
        engine.add_order(Order(3, "SELL", 98.0, 6))

        engine.match_orders()

        self.assertEqual(len(engine.trades), 2)
        self.assertEqual(engine.trades[0]["quantity"], 4)
        self.assertEqual(engine.trades[1]["quantity"], 6)
        self.assertEqual(len(engine.buy_orders), 0)
        self.assertEqual(len(engine.sell_orders), 0)

    def test_duplicate_order_id_is_rejected(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 100.0, 5))

        with self.assertRaises(ValueError):
            engine.add_order(Order(1, "SELL", 95.0, 5))

    def test_invalid_order_id_can_be_reused(self):
        engine = MatchingEngine()

        with self.assertRaises(ValueError):
            engine.add_order(Order(1, "BUY", 0, 5))

        engine.add_order(Order(1, "BUY", 100, 5))

        self.assertEqual(len(engine.buy_orders), 1)

    def test_non_integer_order_id_is_rejected(self):
        engine = MatchingEngine()

        with self.assertRaises((ValueError, TypeError)):
            Order(1.5, "BUY", 100.0, 5)

    def test_non_integer_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "BUY", 100.0, 2.5)

    def test_boolean_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "BUY", 100.0, True)

    def test_nan_price_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "BUY", float("nan"), 5)

    def test_boolean_price_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "BUY", True, 5)

    def test_infinite_price_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "BUY", float("inf"), 5)

    def test_string_price_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "BUY", "abc", 5)

    def test_none_price_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "BUY", None, 5)

    def test_invalid_order_side_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(1, "HOLD", 100.0, 5)

    def test_boolean_order_id_is_rejected(self):
        with self.assertRaises(ValueError):
            Order(True, "BUY", 100.0, 5)

    def test_rejected_order_id_is_not_reserved(self):
        engine = MatchingEngine()

        invalid_order = Order(1, "BUY", 100.0, 5)
        invalid_order.price = 0

        with self.assertRaises(ValueError):
            engine.add_order(invalid_order)

        valid_order = Order(1, "BUY", 100.0, 5)
        engine.add_order(valid_order)

        self.assertEqual(len(engine.buy_orders), 1)

    def test_different_symbols_do_not_match(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 100.0, 5, symbol="CMX/USD"))
        engine.add_order(Order(2, "SELL", 90.0, 5, symbol="ETH/USD"))

        engine.match_orders()

        self.assertEqual(len(engine.trades), 0)
        self.assertEqual(len(engine.buy_orders), 1)
        self.assertEqual(len(engine.sell_orders), 1)

    def test_same_symbol_orders_match(self):
        engine = MatchingEngine()

        engine.add_order(Order(1, "BUY", 100.0, 5, symbol="ETH/USD"))
        engine.add_order(Order(2, "SELL", 95.0, 5, symbol="ETH/USD"))

        engine.match_orders()

        self.assertEqual(len(engine.trades), 1)
        self.assertEqual(engine.trades[0]["symbol"], "ETH/USD")

    def test_symbol_is_normalized(self):
        order = Order(1, "BUY", 100.0, 5, symbol=" eth/usd ")

        self.assertEqual(order.symbol, "ETH/USD")

    def test_different_symbols_do_not_share_trades(self):
        engine = MatchingEngine()

        engine.add_order(
            Order(1, "BUY", 100.0, 5, symbol="CMX/USD")
        )
        engine.add_order(
            Order(2, "SELL", 90.0, 5, symbol="ETH/USD")
        )

        engine.match_orders()

        self.assertEqual(len(engine.trades), 0)
        self.assertEqual(len(engine.buy_orders), 1)
        self.assertEqual(len(engine.sell_orders), 1)

    def test_order_side_is_normalized(self):
        buy_order = Order(101, "buy", 100, 5)
        sell_order = Order(102, "sell", 101, 5)

        self.assertEqual(buy_order.side, "BUY")
        self.assertEqual(sell_order.side, "SELL")

if __name__ == "__main__":
    unittest.main()
