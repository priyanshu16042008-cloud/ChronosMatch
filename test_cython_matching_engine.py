import unittest
import cython_matching_engine


class TestCythonMatchingEngine(unittest.TestCase):

    def test_best_buy_price(self):
        self.assertEqual(
            cython_matching_engine.best_buy_price([100, 120, 110]),
            120.0
        )

    def test_best_sell_price(self):
        self.assertEqual(
            cython_matching_engine.best_sell_price([100, 120, 110]),
            100.0
        )

    def test_empty_buy_prices(self):
        self.assertEqual(
            cython_matching_engine.best_buy_price([]),
            0.0
        )

    def test_empty_sell_prices(self):
        self.assertEqual(
            cython_matching_engine.best_sell_price([]),
            0.0
        )

    def test_single_price(self):
        self.assertEqual(
            cython_matching_engine.best_buy_price([105]),
            105.0
        )
        self.assertEqual(
            cython_matching_engine.best_sell_price([105]),
            105.0
        )


if __name__ == "__main__":
    unittest.main()