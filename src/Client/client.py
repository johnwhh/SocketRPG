import asyncio
import websockets
from Shared.Messages.Message import ClientSetNameMessage

async def hello():
    async with websockets.connect('ws://localhost:9292') as websocket:

        name = input("What's your name? ")
        await websocket.send(ClientSetNameMessage(name))
        # print("> {}".format(name))

        greeting = await websocket.recv()
        # print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())