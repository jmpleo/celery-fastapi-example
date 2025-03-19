import random
import time
import math


class Service:
    def __init__(self):
        pass

    def work(self, n: int):
        if n <= 1:
            return []
        time.sleep(random.randint(1, int(math.log(n))))
        return [random.randint(0, n) for _ in range(0, n)]
