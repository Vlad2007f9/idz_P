import pytest
import asyncio
from structures.idz_3_2 import ResourceCounter, worker


@pytest.mark.asyncio
async def test_race_condition():
    counter = ResourceCounter()
    max = 1000

    task = []
    for _ in range(100):
        task.append(worker(counter, lock=False))

    await asyncio.gather(*task)

    assert counter.value < max


@pytest.mark.asyncio
async def test_atomic_lock():
    counter = ResourceCounter()
    max = 1000

    task = []
    for _ in range(100):
        task.append(worker(counter, lock=True))

    await asyncio.gather(*task)

    assert counter.value == max