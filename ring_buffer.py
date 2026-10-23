
import mmap
import os
import struct


class RingBuffer:
    """
    Fixed-size memory-mapped ring buffer for order data.

    Each record contains:
    Order ID: 8 bytes
    Price:    8 bytes
    Quantity: 8 bytes
    """

    RECORD_FORMAT = "<QdQ"
    RECORD_SIZE = struct.calcsize(RECORD_FORMAT)

    def __init__(self, capacity, filename="orders_buffer.dat"):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        self.capacity = capacity
        self.filename = filename
        self.file = open(filename, "w+b")

        self.file.truncate(capacity * self.RECORD_SIZE)

        self.memory = mmap.mmap(
            self.file.fileno(),
            capacity * self.RECORD_SIZE,
            access=mmap.ACCESS_WRITE,
        )

        self.write_index = 0
        self.read_index = 0
        self.count = 0

    def write(self, order_id, price, quantity):
        if self.count == self.capacity:
            return False

        if (
            not isinstance(order_id, int)
            or isinstance(order_id, bool)
            or not 0 <= order_id <= 0xFFFFFFFFFFFFFFFF
        ):
            raise ValueError("Order ID must be a valid unsigned 64-bit integer")

        if (
            not isinstance(price, (int, float))
            or isinstance(price, bool)
            or not __import__("math").isfinite(price)
            or price < 0
        ):
            raise ValueError("Price must be a finite, non-negative number")

        if (
            not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or not 0 <= quantity <= 0xFFFFFFFFFFFFFFFF
        ):
            raise ValueError("Quantity must be a valid unsigned 64-bit integer")

        offset = self.write_index * self.RECORD_SIZE

        struct.pack_into(
            self.RECORD_FORMAT,
            self.memory,
            offset,
            order_id,
            float(price),
            quantity,
        )

        self.write_index = (self.write_index + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_index * self.RECORD_SIZE

        order_id, price, quantity = struct.unpack_from(
            self.RECORD_FORMAT,
            self.memory,
            offset,
        )

        self.read_index = (self.read_index + 1) % self.capacity
        self.count -= 1

        return {
            "order_id": order_id,
            "price": price,
            "quantity": quantity,
        }

    def close(self):
        if not self.memory.closed:
            self.memory.close()

        if not self.file.closed:
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
