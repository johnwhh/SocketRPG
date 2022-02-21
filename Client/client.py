import websockets
import asyncio
import sys
import os
import threading
try:
    import msvcrt
except:
    import getch

import curses

sys.path.append(sys.path[0] + '/..')

from Shared.Message import Message

class Client:
    def __init__(self):
        self.messageQueue = []
        
    async def _listenForMessages(self):
        async for message in self.websocket:
            await self._handleMessage(message)            

    async def _handleMessage(self, message):
        self._refreshMap(message)

    def _refreshMap(self, map):
        if sys.platform == "linux" or sys.platform == "darwin":
            os.system("clear")
        else:
            os.system("cls")

        os.system(f"echo '{map}'")

    async def _sendMessage(self, message):

        await self.websocket.send(message.value)

    async def _handleNextKeyPress(self):
        try:
            key = self.messageQueue.pop()
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
        except IndexError:
            # no message to read
            pass
    
    def _getCurrentKey(self):
        curKey = None
        if sys.platform.lower == 'win32':
            curKey = msvcrt.getch()
        else:
            curKey = getch.getch()
        return curKey

    def _checkInput(self):
        keyPressed = self._getCurrentKey() 
        if keyPressed == None:
            return
        if keyPressed == 'q':
            return 
        self.messageQueue.append(keyPressed)

    async def _update(self):
        while True:
            try:
                self._checkInput()
                await self._listenToServer()
                await self._listenToKeyboard()
            except:
                continue

    async def _listenToServer(self):
        try:
            await asyncio.wait_for(self._listenForMessages(), 0.2)
        except:
            return

    async def _listenToKeyboard(self):
        try:
            await asyncio.wait_for(self._handleNextKeyPress(), 0.2)
        except:
            return

    async def _connectToServer(self):
        async with websockets.connect('ws://localhost:9292') as websocket:
            self.websocket = websocket
            await self.websocket.send(Message.CONNECT.value)
            asyncio.get_event_loop().run_until_complete(await self._update())


    def start(self):
        asyncio.get_event_loop().run_until_complete(self._connectToServer())


if __name__ == "__main__":
    client = Client()
    client.start()
