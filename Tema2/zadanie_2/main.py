import asyncio
import time

from parser import main
from database.queries.orm import create_tables


if __name__ == '__main__':
    asyncio.run(create_tables())
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Скрипт отработал за {end - start:.2f} секунд")

