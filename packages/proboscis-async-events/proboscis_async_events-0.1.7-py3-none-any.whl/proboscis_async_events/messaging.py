from asyncio import Event
from dataclasses import dataclass, field

import pampy


@dataclass
class _Item:
    header: str
    value: object


class MessageClosed(Exception):
    pass


class MessageUnsubscribed(Exception):
    pass


@dataclass
class Subscriber:
    src_handle: "Messages"

    def __post_init__(self):
        self.value_set = Event()
        self.value_set.clear()
        self.value_empty = Event()
        self.value_empty.set()
        self.entered = Event()
        self.message = _Item("waiting", None)

    async def __aenter__(self):
        self.entered.set()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.unsubscribe()
        self.entered.clear()


    async def tell(self, message: _Item):
        assert self.message.header != 'end', "Cannot publish to a closed subscriber"
        await self.value_empty.wait()
        self.message = message
        self.value_empty.clear()
        # print(f'Subscriber{id(self)}: setting value_set signal')
        self.value_set.set()
        # print(f'Subscriber: value_set signal set:{self.value_set.is_set()}:{id(self.value_set)}')
        match message:
            case _Item('item', value):
                # wait for subscriber to consume the message
                # print('Subscriber: waiting for value_empty signal')
                await self.value_empty.wait()
            case _Item('end' | 'unsubscribe', None):
                # print(f"subscriber: closing subscriber due to {message.header}")
                pass
            case _:
                raise ValueError(f"Invalid message type {message}")

    async def get_raw(self):
        # print(f'Subscriber{id(self)}: waiting for value_set signal:{self.value_set.is_set()}:{id(self.value_set)}')
        assert self.entered.is_set(), "Subscriber must be entered with async with statement"
        await self.value_set.wait()
        # print('Subscriber: waited for value_set signal')
        res = self.message
        self.message = _Item("waiting", None)
        self.value_set.clear()
        self.value_empty.set()
        # print('Subscriber: value_set signal cleared')
        return res

    async def get(self):
        res = await self.get_raw()
        match res:
            case _Item('end', None):
                raise MessageClosed()
            case _Item('unsubscribe', None):
                raise MessageUnsubscribed()
            case _Item('item', value):
                return value

    async def unsubscribe(self):
        res = await self.src_handle.unsubscribe(self)
        # print('subscriber: unsubscribed')
        return res

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
            # print('Subscriber: waiting for message')
            message = await self.get()

            # print(f'Subscriber: matching {message} against {pattern}')

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
        assert not isinstance(message, _Item), "Cannot publish a _Item"
        #print(f'Messages: publishing {message} to {len(self.subscribers)} subscribers')
        for subscriber in list(self.subscribers):
            await subscriber.tell(_Item('item', message))
        #print(f'Messages: published {message} to {len(self.subscribers)} subscribers')

    async def unsubscribe(self, subscriber: Subscriber):
        #print(f'Messages: unsubscribing {id(subscriber)} from {self.subscribers}')
        self.subscribers.remove(subscriber)
        await subscriber.tell(_Item('unsubscribe', None))
        #print(f'Messages: unsubscription done for {id(subscriber)}')
        #print(f'Messages: remaining subscribers:{[id(s) for s in self.subscribers]}')

    async def close(self):
        for subscriber in list(self.subscribers):
            #print(f'Messages: closing subscriber:{subscriber}')
            await subscriber.tell(_Item('end', None))
            #print('Messages: closed subscriber')
