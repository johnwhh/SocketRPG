import sys
sys.path.append(sys.path[0] + '\..')

import asyncio
import websockets

from Shared.Message import ClientSetNameMessage

async def hello():
    async with websockets.connect('ws://localhost:9292') as websocket:

        name = input("What's your name? ")
        nameMessage = ClientSetNameMessage(name)

        await websocket.send(nameMessage)
        # print("> {}".format(name))

        greeting = await websocket.recv()
        # print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())
# C:\Git\socketrpg\Shared\Messages\Message.py
# Shared\Messages\Message.py