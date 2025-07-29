from Workers.Service.HealthService import coroutine_get_health

from Workers.Service.Transaction import run_workers

import asyncio

async def main():
    worker_health = asyncio.create_task(coroutine_get_health())
    worker_transactions = asyncio.create_task(run_workers())

    await asyncio.gather(worker_health, worker_transactions)


if __name__ == "__main__":
    asyncio.run(main())
