import asyncio
from asyncio import Event
from dataclasses import dataclass, field
from queue import Empty

import pampy


@dataclass
class _Item:
    header: str
    value: object


class MessageClosed(Exception):
    pass


@dataclass
class Subscriber:
    src_handle: "Messages"

    def __post_init__(self):
        self.value_set = Event()
        self.value_empty = Event()
        self.message = _Item("waiting", None)

    async def tell(self, message: _Item):
        assert self.message.header != 'end', "Cannot publish to a closed subscriber"
        await self.value_empty.wait()
        match message:
            case _Item('item', value):
                self.message = message
                self.value_empty.clear()
                self.value_set.set()
                await self.value_empty.wait()
            case _Item('end', None):
                self.message = message
                self.value_empty.clear()
                self.value_set.set()

    async def get_raw(self):
        await self.value_set.wait()
        res = self.message
        self.message = _Item("waiting", None)
        self.value_set.clear()
        self.value_empty.set()
        return res

    async def get(self):
        res = await self.get_raw()
        match res:
            case _Item('end', None):
                raise MessageClosed()
            case _Item('item', value):
                return value

    def unsubscribe(self):
        self.src_handle.unsubscribe(self)

    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self.get_raw()
        match item:
            case _Item('end', None):
                raise StopAsyncIteration
            case _Item('item', value):
                return value

    async def wait(self, pattern):
        from pampy import _
        matched = False
        while not matched:
            message = await self.get()

            def on_match(*args):
                nonlocal matched
                matched = True

            pampy.match(message,
                        pattern, on_match,
                        _, lambda *args: None
                        )
        return message


@dataclass
class Messages:
    subscribers: list[Subscriber] = field(default_factory=list)

    def subscribe(self) -> Subscriber:
        subscriber = Subscriber(self)
        self.subscribers.append(subscriber)
        return subscriber

    async def publish(self, message):
        for subscriber in self.subscribers:
            await subscriber.tell(message)

    def unsubscribe(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    async def close(self):
        await self.publish(None)
