import asyncio
import pytest

from structures.idz_2_1 import recursive_search

@pytest.mark.asyncio
async def  test_recursive_search(tmp_path):

    dir1 = tmp_path / "logs_folder"
    dir1.mkdir()

    dir2 = dir1 / "nested_folder"
    dir2.mkdir()

    log_file1 = tmp_path / "root_debug.log"
    log_file1.write_text("some log data")

    log_file2 = dir1 / "dir1_debug.log"
    log_file2.write_text("dir1 log data")

    txt_file = dir2 / "dir2_txt_debug.txt"
    txt_file.write_text("this is not a log file")


    for i in range(1, 16):
        log_file = tmp_path / f"test_log_{i}.log"
        log_file.write_text("log files")

    stop_event = asyncio.Event()
    stop_event.set()
    
    results = []

    await recursive_search(str(tmp_path), ".log", stop_event, results)

    expected_count = 2
    assert len(results) == expected_count

    assert str(log_file1) in results
    assert str(log_file2) in results

    assert str(txt_file) not in results






