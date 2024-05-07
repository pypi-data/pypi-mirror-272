import asyncio
from asyncio import Event, Lock, Queue, TaskGroup
from dataclasses import dataclass, field
from loguru import logger

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
        self.unsubscribed = Event()
        self.message = _Item("waiting", None)
        self.value_empty_wait_count = 0

    async def __aenter__(self):
        self.entered.set()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.trace(f"Subscriber: exiting {id(self)} with {exc_type} {exc_val} {exc_tb}")
        await self.unsubscribe()
        self.entered.clear()

    async def _set_message(self, msg: _Item):
        self.message = msg
        self.value_set.set()
        self.value_empty.clear()
        logger.trace(f'Subscriber({id(self)}: message set: {str(msg)[:100]}')

    async def _consume_msg(self):
        self.message = _Item('waiting', None)
        self.value_set.clear()
        self.value_empty.set()
        logger.trace(f"Subscriber({id(self)}: consumed message.")

    async def wait_empty(self):
        self.value_empty_wait_count += 1
        logger.trace(f"waiting for value_empty signal {self.value_empty_wait_count} times.")
        await self.value_empty.wait()
        self.value_empty_wait_count -= 1
        logger.trace(f"remaining value_empty_wait_count:{self.value_empty_wait_count}")

    async def tell(self, message: _Item):
        logger.trace(f"Subscriber({id(self)})telling message to subscriber. {str(message)[:100]}")
        assert not self.unsubscribed.is_set(), "Cannot tell to an unsubscribed subscriber"
        logger.trace(
            f'Subscriber({id(self)}): waiting for value_empty signal({self.value_empty.is_set()}) to tell. ({str(message)[:100]})')
        await self.wait_empty()
        logger.trace(f'Subscriber({id(self)}): value_empty signal received')
        await self._set_message(message)
        match message:
            case _Item('item', value):
                # wait for subscriber to consume the message
                logger.trace(
                    f'Subscriber({id(self)}: waiting for value_empty signal to have {str(message)[:50]} consumed.')
                await self.wait_empty()
                assert self.value_empty.is_set(), "Value must be set after wait, right???"
                # some other tasks that awaits value_empty has immediately cleared it?
                logger.trace(f'Subscriber({id(self)}: value has been consumed!({self.value_empty.is_set()})')
            case _Item('end', None):
                logger.trace(f"subscriber({id(self)}: closing subscriber due to {message.header}")
            case _Item('unsubscribe'):
                logger.trace(f"subscriber({id(self)}: closing subscriber due to {message.header}")
                self.unsubscribed.set()
            case _:
                raise ValueError(f"Invalid message type {message}")
        logger.success(f"Subscriber({id(self)}): message told. ({str(message)[:100]})")

    async def get_raw(self):
        logger.trace(
            f'Subscriber{id(self)}: waiting for value_set signal:{self.value_set.is_set()}:{id(self.value_set)}')
        assert self.entered.is_set(), "Subscriber must be entered with async with statement"
        await self.value_set.wait()
        logger.trace('Subscriber: waited for value_set signal')
        res = self.message
        await self._consume_msg()
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
        await self._consume_msg()
        res = await self.src_handle.unsubscribe(self)
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
            logger.trace('Subscriber: waiting for message')
            message = await self.get()

            logger.trace(f'Subscriber: matching {message} against {pattern}')

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

    def __post_init__(self):
        self.publishing = False
        self.msg_queue = Queue()

    def subscribe(self) -> Subscriber:
        subscriber = Subscriber(self)
        self.subscribers.append(subscriber)
        return subscriber

    async def publish(self, message):
        self.msg_queue.put_nowait(('publish', message))
        await self.process_events()

    async def process_events(self):
        if self.publishing:
            return
        self.publishing = True
        while self.msg_queue.qsize() > 0:
            (kind, msg) = self.msg_queue.get_nowait()
            match kind:
                case 'publish':
                    assert not isinstance(msg, _Item), "Cannot publish a _Item"
                    logger.trace(f'Messages: publishing {str(msg)[:100]} to {len(self.subscribers)} subscribers')
                    async with TaskGroup() as tg:
                        for sub in self.subscribers:
                            tg.create_task(sub.tell(_Item('item', msg)))
                    logger.trace(f'Messages: published {str(msg)[:100]} to {len(self.subscribers)} subscribers')
                case 'unsubscribe':
                    subscriber = msg
                    logger.trace(f'Messages: unsubscribing {id(subscriber)} from {[id(s) for s in self.subscribers]}')
                    # self.subscribers.remove(subscriber) remove doesn't work with id, so we need alternative implementation.
                    self.subscribers = [s for s in self.subscribers if id(s) != id(subscriber)]
                    await subscriber.tell(_Item('unsubscribe', None))
                    logger.trace(f'Messages: unsubscription done for {id(subscriber)}')
                    logger.trace(f'Messages: remaining subscribers:{[id(s) for s in self.subscribers]}')
                case 'end':
                    async with TaskGroup() as tg:
                        for sub in self.subscribers:
                            tg.create_task(sub.tell(_Item('end', None)))
                case _:
                    raise ValueError(f"Invalid message type {kind}")

        self.publishing = False

    async def unsubscribe(self, subscriber: Subscriber):
        self.msg_queue.put_nowait(('unsubscribe', subscriber))
        await self.process_events()

    async def close(self):
        self.msg_queue.put_nowait(('end', None))
        await self.process_events()
