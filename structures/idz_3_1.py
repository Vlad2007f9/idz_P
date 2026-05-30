import asyncio
import httpx
import json

async def check_resource(client, name, url):
    print(f"--- Перевірка resource {name} почалася ---")
    # Реальний запит до зовнішнього ресурсу, який імітує затримку в 1 секундуresponse = await client.get(url)

    max = 3
    response = None

    for attempt in range(1, max + 1):
        try:
            response = await client.get(url)

            if response.status_code == 503:
                print(f"Attempt {attempt}/{max} Server {name} returned 503")

                if attempt == max:
                    break

                await asyncio.sleep(1)
                continue
            break

        except httpx.TimeoutException as e:
            print(f"Attempt {attempt}/{max} Network error on {name}: {e}")

            if attempt == max:
                    break

            await asyncio.sleep(1)

    if response is not None and response.status_code == 200:   
        try:
            data = response.json()
            print(f"--- Resource {name} перевірено (Статус: {response.status_code})---")
            return f"Дані від {name}"
        except json.JSONDecodeError:
            print(f"ERROR Corrupted data from {name}")
            return f"Broken data from {name}"
    else:
            status = response.status_code if response is not None else "There is no connection"
            print(f"--- CRITICAL Resource {name} did not respond after {max} attempts (Status: {status}) ---")
            return f"Server error {name}"