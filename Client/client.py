import websockets
import asyncio
import sys
import os
from threading import Thread

sys.path.append(sys.path[0] + '/..')

from Shared.Message import Message

class Client:
    async def _listenForMessages(self):
        async for message in self.websocket:
            await self._handleMessage(message)

    async def _handleMessage(self, message):
        self._refreshMap(message)
        await self._handleInput()

    def _refreshMap(self, map):
        if sys.platform == "linux" or sys.platform == "darwin":
            os.system("clear")
        else:
            os.system("cls")

        os.system(f"echo '{map}'")

    async def _sendMessage(self, message):
        await self.websocket.send(message.value)

    async def _handleInput(self):
        key = input("Next move:")
        if key == "w":
            await self._sendMessage(Message.UP)
        elif key == "s":
            await self._sendMessage(Message.DOWN)
        elif key == "a":
            await self._sendMessage(Message.LEFT)
        elif key == "d":
            await self._sendMessage(Message.RIGHT)
        elif key == "h":
            await self._sendMessage(Message.HEAL)
        elif key == "q":
            await self._sendMessage(Message.DISCONNECT)
        else:
            await self._handleInput()

    async def _handleKeyboardPress(self, key):
        if key == "w":
            await self._sendMessage(Message.UP)
        elif key == "s":
            await self._sendMessage(Message.DOWN)
        elif key == "a":
            await self._sendMessage(Message.LEFT)
        elif key == "d":
            await self._sendMessage(Message.RIGHT)
        elif key == "h":
            await self._sendMessage(Message.HEAL)
        elif key == "q":
            await self._sendMessage(Message.DISCONNECT)

    async def _connectToServer(self):
        async with websockets.connect('ws://localhost:9292') as websocket:
            await websocket.send(Message.CONNECT.value)
            self.websocket = websocket

            asyncio.get_event_loop().run_until_complete(await self._listenForMessages())

    def start(self):
        asyncio.get_event_loop().run_until_complete(self._connectToServer())


if __name__ == "__main__":
    client = Client()
    client.start()
