import asyncio
import os

async def recursive_search(path, extension, stop_event, results):
    """
    Рекурсивно шукає файли.
    results - список, куди додаються знайдені шляхи.
    """
    print(f"[Пошук] Розпочато сканування: {path}")
    fol_cnt = 0

    for root, dirs, files in os.walk(path):
        # ПЕРЕВІРКА: чи не надійшов сигнал зупинки
        if stop_event.is_set():
            print("[Пошук] Отримано сигнал зупинки. Перериваємося...")
            break

        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                results.append(full_path)

        fol_cnt += 1
        if fol_cnt % 10000 == 0:
            print(f"[Progress] already scanned {fol_cnt} found {len(results)} files")

# "Поступаємося" чергою іншим задачам
        await asyncio.sleep(0)