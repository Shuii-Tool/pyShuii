import asyncio
import tqdm
import os

DISABLE = os.environ.get(
    "ENV") == "PROD" and True or False


async def traceCast(desc, fn, tasks):
    _tasks = [
        asyncio.create_task(
            fn(
                **tasks[task]
            )
        ) for task in range(len(tasks))
    ]

    return [
        await t for t in tqdm.tqdm(
            asyncio.as_completed(_tasks),
            total=len(_tasks),
            desc=desc,
            disable=DISABLE
        )
    ]
