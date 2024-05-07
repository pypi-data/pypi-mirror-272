import asyncio
from asyncio import TaskGroup

from proboscis_async_events import Messages


def test_run_messages():
    messages = Messages()

    async def test_pub_sub():
        await messages.publish("hello")

        async def subber1(sub):
            async for message in sub:
                print(f"got message:{message}")
                if message == 'end':
                    return
        async def subber2(sub):
            import pampy
            print(f'waiting for world:sub-{id(sub)}')
            ev = await sub.wait(pampy._)
            print(f'got world:{ev}')
            print('waiting for end')
            ev = await sub.wait('end')
            print(f'got end:{ev}')
            print('unsubscribing')
            await sub.unsubscribe()


        async with TaskGroup() as tg:
            #tg.create_task(subber1())
            # hmm, sub needs to be created before the messages starts.
            tg.create_task(subber2(messages.subscribe()))
            print('publishing world')
            await messages.publish("world")
            print('publishing end')
            await messages.publish('end')
            print('publishing messages finished')
    asyncio.run(test_pub_sub())


