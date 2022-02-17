import websockets
import asyncio
import sys
sys.path.append(sys.path[0] + '/..')

from Shared.Message import ClientSetNameMessage

async def listenForMessages(websocket):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)


async def connectToServer():
    async with websockets.connect('ws://localhost:9292') as websocket:

        name = input("What's your name? ")
        nameMessage = ClientSetNameMessage(name)

        await websocket.send(nameMessage.toJSON())

        asyncio.get_event_loop().run_until_complete(await listenForMessages(websocket))

asyncio.get_event_loop().run_until_complete(connectToServer())
