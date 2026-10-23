
import asyncio
import random

from ring_buffer import RingBuffer


async def generate_orders(buffer, total_orders=1000):
    """Generate mock Buy/Sell orders asynchronously."""

    accepted = 0
    rejected = 0

    for order_id in range(1, total_orders + 1):
        price = round(random.uniform(90, 110), 2)
        quantity = random.randint(1, 100)

        success = buffer.write(order_id, price, quantity)

        if success:
            accepted += 1
        else:
            rejected += 1

        # Allow other asynchronous tasks to run.
        if order_id % 100 == 0:
            await asyncio.sleep(0)

    return accepted, rejected


async def main():
    total_orders = 1000

    # Start with enough capacity for this test.
    with RingBuffer(capacity=total_orders) as buffer:
        accepted, rejected = await generate_orders(
            buffer,
            total_orders,
        )

        print(f"Orders generated: {total_orders}")
        print(f"Orders accepted: {accepted}")
        print(f"Orders rejected: {rejected}")
        print(f"Orders currently in buffer: {buffer.count}")

        # Verify that the first order can be read.
        first_order = buffer.read()
        print(f"First order read: {first_order}")
        print(f"Orders remaining: {buffer.count}")


if __name__ == "__main__":
    asyncio.run(main())
