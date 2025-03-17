import time
import random


class Service:
    def __init__(self):
        pass

    def work(self, q: str):
        total = random.randint(0, 100_000)
        time.sleep(random.randint(1, 5))
        return {
            "total": total,
            "data": [
                [f"data_{i}"]
                for i in range(total)
            ]
        }
