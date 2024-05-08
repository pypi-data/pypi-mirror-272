import asyncio
from asyncio import TaskGroup

from proboscis_async_events import Messages
from loguru import logger


def test_run_messages():
    messages = Messages()

    async def test_pub_sub():
        await messages.publish("hello")

        async def subber1(sub):
            async with sub:
                async for message in sub:
                    logger.debug(f"got message:{message}")
                    if message == 'end':
                        # ah, if you stop the iterator at this point,
                        # this messages waits for the value to be consumed...
                        # how can I stop that?
                        # maybe timeout? no,,,
                        # but how can a messages tell that it has finished consuming.
                        return
        async def subber2(sub):
            async with sub:
                import pampy
                logger.debug(f'waiting for world:sub-{id(sub)}')
                ev = await sub.wait('world')
                logger.debug(f'got world:{ev}')
                logger.debug('waiting for end')
                ev = await sub.wait('end')
                logger.debug(f'got end:{ev}')
                logger.debug('unsubscribing')
                logger.debug('unsubscribed')

        async def subber3():
            async with messages.subscribe() as sub:
                async for message in sub:
                    logger.info(f"subber 3 got message:{message}")
                    await asyncio.sleep(3)
                    logger.warning(f"waited 3 seconds")
                    #raise RuntimeError('End error')


        async with TaskGroup() as tg:
            tg.create_task(subber1(messages.subscribe()))
            tg.create_task(subber2(messages.subscribe()))
            tg.create_task(subber3())
            #await asyncio.sleep(0 )
            logger.debug('publishing world')
            await messages.publish("world")
            logger.debug('publishing end')
            await messages.publish('end')
            logger.debug('publishing another event')
            await messages.publish('another event')
            logger.debug('closing messages')
            await messages.close()
            logger.debug('publishing messages finished')
    asyncio.run(test_pub_sub())


