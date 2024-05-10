import asyncio


class AsyncCounter:
    def __init__(self):
        self.counter = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        async with self.lock:
            self.counter += 1

    async def decrement(self):
        async with self.lock:
            self.counter -= 1

    async def get(self):
        async with self.lock:
            return self.counter
