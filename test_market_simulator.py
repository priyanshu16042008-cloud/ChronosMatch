
import asyncio
import os
import tempfile
import unittest

from ring_buffer import RingBuffer
from market_simulator import generate_orders


class TestMarketSimulator(unittest.TestCase):

    def setUp(self):
        temp = tempfile.NamedTemporaryFile(delete=False)
        self.filename = temp.name
        temp.close()

        self.buffer = RingBuffer(100, self.filename)

    def tearDown(self):
        self.buffer.close()

        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_all_orders_accepted(self):
        accepted, rejected = asyncio.run(
            generate_orders(self.buffer, 100)
        )

        self.assertEqual(accepted, 100)
        self.assertEqual(rejected, 0)
        self.assertEqual(self.buffer.count, 100)

    def test_buffer_capacity_respected(self):
        accepted, rejected = asyncio.run(
            generate_orders(self.buffer, 150)
        )

        self.assertEqual(accepted, 100)
        self.assertEqual(rejected, 50)
        self.assertEqual(self.buffer.count, 100)

    def test_orders_have_valid_values(self):
        asyncio.run(generate_orders(self.buffer, 10))

        order = self.buffer.read()

        self.assertIsNotNone(order)
        self.assertGreater(order["order_id"], 0)
        self.assertGreaterEqual(order["price"], 90)
        self.assertLessEqual(order["price"], 110)
        self.assertGreaterEqual(order["quantity"], 1)
        self.assertLessEqual(order["quantity"], 100)


if __name__ == "__main__":
    unittest.main()
