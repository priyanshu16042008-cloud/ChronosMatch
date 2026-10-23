
import mmap
import os
import struct
import tempfile
import multiprocessing as mp

RECORD_FORMAT = "<QdQ"
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)


def producer(filename, capacity, total_orders,
             write_index, read_index, count, condition):

    with open(filename, "r+b") as file:
        memory = mmap.mmap(
            file.fileno(),
            capacity * RECORD_SIZE,
            access=mmap.ACCESS_WRITE
        )

        try:
            for order_id in range(1, total_orders + 1):
                price = 100.0 + (order_id % 10)
                quantity = order_id % 100 + 1

                with condition:
                    while count.value == capacity:
                        condition.wait()

                    offset = write_index.value * RECORD_SIZE

                    struct.pack_into(
                        RECORD_FORMAT,
                        memory,
                        offset,
                        order_id,
                        price,
                        quantity
                    )

                    write_index.value = (
                        write_index.value + 1
                    ) % capacity

                    count.value += 1
                    condition.notify_all()

        finally:
            memory.close()


def consumer(filename, capacity, total_orders,
             write_index, read_index, count,
             consumed, errors, condition):

    with open(filename, "r+b") as file:
        memory = mmap.mmap(
            file.fileno(),
            capacity * RECORD_SIZE,
            access=mmap.ACCESS_WRITE
        )

        try:
            for expected_id in range(1, total_orders + 1):
                with condition:
                    while count.value == 0:
                        condition.wait()

                    offset = read_index.value * RECORD_SIZE

                    order_id, price, quantity = struct.unpack_from(
                        RECORD_FORMAT,
                        memory,
                        offset
                    )

                    read_index.value = (
                        read_index.value + 1
                    ) % capacity

                    count.value -= 1
                    consumed.value += 1

                    if order_id != expected_id:
                        errors.value += 1

                    condition.notify_all()

        finally:
            memory.close()


def main():
    print("1. Main function started", flush=True)

    capacity = 64
    total_orders = 10_000

    # Use one multiprocessing context for all shared objects.
    ctx = mp.get_context("spawn")

    write_index = ctx.Value("i", 0, lock=False)
    read_index = ctx.Value("i", 0, lock=False)
    count = ctx.Value("i", 0, lock=False)
    consumed = ctx.Value("i", 0, lock=False)
    errors = ctx.Value("i", 0, lock=False)

    condition = ctx.Condition()

    with tempfile.TemporaryDirectory() as temp_dir:
        filename = os.path.join(temp_dir, "orders.dat")

        # Create the memory-mapped file before starting processes.
        with open(filename, "w+b") as file:
            file.truncate(capacity * RECORD_SIZE)

        print("2. Shared file created", flush=True)

        consumer_process = ctx.Process(
            target=consumer,
            args=(
                filename, capacity, total_orders,
                write_index, read_index, count,
                consumed, errors, condition
            )
        )

        producer_process = ctx.Process(
            target=producer,
            args=(
                filename, capacity, total_orders,
                write_index, read_index, count, condition
            )
        )

        print("3. Starting consumer", flush=True)
        consumer_process.start()

        print("4. Starting producer", flush=True)
        producer_process.start()

        producer_process.join()
        consumer_process.join()

        print("\n--- IPC Test Results ---")
        print("Producer exit code:", producer_process.exitcode)
        print("Consumer exit code:", consumer_process.exitcode)
        print("Orders produced:", total_orders)
        print("Orders consumed:", consumed.value)
        print("Order sequence errors:", errors.value)
        print("Final buffer count:", count.value)

        if producer_process.exitcode != 0:
            raise RuntimeError("Producer process failed")

        if consumer_process.exitcode != 0:
            raise RuntimeError("Consumer process failed")

        if consumed.value != total_orders or errors.value != 0:
            raise RuntimeError("IPC validation failed")

        if count.value != 0:
            raise RuntimeError("Buffer should be empty")

        print("IPC test PASSED!")


if __name__ == "__main__":
    mp.freeze_support()
    main()
