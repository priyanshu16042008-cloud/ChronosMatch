
import os
import tempfile
import unittest

from ring_buffer import RingBuffer


class TestRingBuffer(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(delete=False)
        self.filename = self.temp.name
        self.temp.close()

        self.buffer = RingBuffer(2, self.filename)

    def tearDown(self):
        self.buffer.close()
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_write_and_read(self):
        self.assertTrue(self.buffer.write(1, 95.5, 10))

        order = self.buffer.read()

        self.assertEqual(order["order_id"], 1)
        self.assertEqual(order["price"], 95.5)
        self.assertEqual(order["quantity"], 10)

    def test_empty_buffer(self):
        self.assertIsNone(self.buffer.read())

    def test_full_buffer(self):
        self.assertTrue(self.buffer.write(1, 100, 5))
        self.assertTrue(self.buffer.write(2, 101, 6))
        self.assertFalse(self.buffer.write(3, 102, 7))

    def test_fifo_order(self):
        self.buffer.write(1, 100, 5)
        self.buffer.write(2, 101, 6)

        self.assertEqual(self.buffer.read()["order_id"], 1)
        self.assertEqual(self.buffer.read()["order_id"], 2)

    def test_reuse_after_read(self):
        self.buffer.write(1, 100, 5)
        self.buffer.write(2, 101, 6)
        self.buffer.read()

        self.assertTrue(self.buffer.write(3, 102, 7))
        self.assertEqual(self.buffer.read()["order_id"], 2)
        self.assertEqual(self.buffer.read()["order_id"], 3)


if __name__ == "__main__":
    unittest.main()
