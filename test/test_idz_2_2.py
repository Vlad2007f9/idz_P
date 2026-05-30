import asyncio
import pytest

from structures.idz_2_2 import recursive_search

@pytest.mark.asyncio
async def  test_recursive_search(tmp_path):

    for i in range(1, 16):
        log_file = tmp_path / f"test_log_{i}.log"
        log_file.write_text("log files")

    stop_event = asyncio.Event()
    stop_event.set()
    
    results = []

    await recursive_search(str(tmp_path), ".log", stop_event, results)

    expected_count = 0
    assert len(results) == expected_count

    assert results == []
