import random
import asyncio


class Service:
    def __init__(self):
        pass

    async def work(self, q: str):
        total = random.randint(0, 100_000)
        await asyncio.sleep(random.randint(1, 5))
        return {
            "total": total,
            "data": [
                [f"data_{i}"]
                for i in range(total)
            ]
        }
