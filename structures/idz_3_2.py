import time
import asyncio
import random

class ResourceCounter:
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self, use_lock=False):

        if use_lock is False:
            current = self.value
            await asyncio.sleep(0)
            self.value = current + 1
        else:
            async with self.lock:
                current = self.value
                await asyncio.sleep(0)
                self.value = current + 1

async def worker(counter, lock=False):
    for _ in range(10):
        await counter.increment(use_lock=lock)    




async def producer(q):
    print("[Producer] Starting log generation: ")

    for i in range(1, 21):
        await q.put(f"Log message {i}")
        print(f"[Producer] Generated and added to the queue Log message {i}")

        await asyncio.sleep(random.uniform(0.1, 0.3))


    await q.put(None)
    await q.put(None)



async def consumer(c_id, q, stats):
    print(f"[Consumer {c_id}] Started, waiting for logs")

    pr_cnt = 0

    while True:
        message = await q.get()

        if message is None:
            print(f"[Consumer {c_id}] Received token 'None' Terminating")
            break

        print(f"[Consumer {c_id}] Started processing: {message}")
        await asyncio.sleep(0.5)
        print(f"[Consumer {c_id}] [OK] Processing completed: {message}")

        pr_cnt += 1

    stats[c_id] = pr_cnt



async def main():
    queue = asyncio.Queue()

    stats = {}


    start = time.perf_counter()

    p_task = asyncio.create_task(producer(queue))


    await asyncio.gather(p_task, consumer(1, queue, stats), consumer(2, queue, stats))

    end = time.perf_counter()

    print("\nReport: ")

    print(f"Total system uptime: {end - start} seconds")
    for id, count in sorted(stats.items()):
        [print(f"Consumer {id} successfully processed: {count} messages")]
    print(f"Total messages processed: {sum(stats.values())} of 20")


if __name__ == "__main__":
    asyncio.run(main())
    