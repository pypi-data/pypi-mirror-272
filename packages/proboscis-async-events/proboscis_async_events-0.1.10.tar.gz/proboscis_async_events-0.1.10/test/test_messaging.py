import asyncio
from asyncio import TaskGroup

from proboscis_async_events import Messages


def test_run_messages():
    messages = Messages()

    async def test_pub_sub():
        await messages.publish("hello")

        async def subber1(sub):
            async with sub:
                async for message in sub:
                    print(f"got message:{message}")
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
                print(f'waiting for world:sub-{id(sub)}')
                ev = await sub.wait('world')
                print(f'got world:{ev}')
                print('waiting for end')
                ev = await sub.wait('end')
                print(f'got end:{ev}')
                print('unsubscribing')
                print('unsubscribed')

        async def subber3():
            async with messages.subscribe() as sub:
                async for message in sub:
                    print(f"got message:{message}")
                    #raise RuntimeError('End error')


        async with TaskGroup() as tg:
            tg.create_task(subber1(messages.subscribe()))
            tg.create_task(subber2(messages.subscribe()))
            tg.create_task(subber3())
            print('publishing world')
            await messages.publish("world")
            print('publishing end')
            await messages.publish('end')
            print('publishing another event')
            await messages.publish('another event')
            print('closing messages')
            await messages.close()
            print('publishing messages finished')
    asyncio.run(test_pub_sub())


