

from unittest import IsolatedAsyncioTestCase
from sourceplus_sdk.libs import AsyncCounter


class TestLibs(IsolatedAsyncioTestCase):
    async_counter = AsyncCounter()

    async def asyncSetUp(self) -> None:
        # reset the counter before each test
        self.async_counter.counter = 0

    async def test_increment(self):
        self.assertEqual(self.async_counter.counter, 0)
        await self.async_counter.increment()
        self.assertEqual(self.async_counter.counter, 1)

    async def test_decrement(self):
        await self.async_counter.increment()
        self.assertEqual(self.async_counter.counter, 1)
        await self.async_counter.decrement()
        self.assertEqual(self.async_counter.counter, 0)

    async def test_get(self):
        self.assertEqual(self.async_counter.counter, 0)
        await self.async_counter.increment()
        self.assertEqual(self.async_counter.counter, 1)
        self.assertEqual(await self.async_counter.get(), 1)
        await self.async_counter.decrement()
        self.assertEqual(self.async_counter.counter, 0)
        self.assertEqual(await self.async_counter.get(), 0)



