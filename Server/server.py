import asyncio
import websockets
from game import Game, Direction
from enum import Enum

import sys

sys.path.append(sys.path[0] + "/..")

from Shared.Message import Message

class Server:
    def __init__(self):
        self.game = Game()
        self.sockets = dict()
        self.playerIdDict = dict()

    async def _listenForMessages(self, websocket, path):
        async for message in websocket:
            await self._handleMessage(message, websocket)

    async def _handleMessage(self, message, websocket):
        if message == Message.CONNECT.value:
            self.sockets[websocket.id] = websocket
            id = self._getAvailablePlayerId()
            self.playerIdDict[websocket.id] = id
            self.game.addNewPlayer(id)
            print(f"Added player {id} with socket uuid {websocket.id}")
        elif message == Message.LEFT.value:
            self.game.movePlayer(
                self.playerIdDict[websocket.id], Direction.LEFT)
            print(f"Player with socket uuid {websocket.id} moved left")
        elif message == Message.RIGHT.value:
            self.game.movePlayer(
                self.playerIdDict[websocket.id], Direction.RIGHT)
            print(f"Player with socket uuid {websocket.id} moved right")
        elif message == Message.UP.value:
            self.game.movePlayer(self.playerIdDict[websocket.id], Direction.UP)
            print(f"Player with socket uuid {websocket.id} moved up")
        elif message == Message.DOWN.value:
            self.game.movePlayer(
                self.playerIdDict[websocket.id], Direction.DOWN)
            print(f"Player with socket uuid {websocket.id} moved down")
        elif message == Message.HEAL.value:
            self.game.healPlayer(self.playerIdDict[websocket.id])
            print(f"Player with socket uuid {websocket.id} healed")
        elif message == Message.DISCONNECT.value:
            await websocket.send("Disconnecting from the server...")
            del self.playerIdDict[websocket.id]
            del self.sockets[websocket.id]
            return

        print(self.game.getGlobalMap())
        await self._broadcastMap()

    async def _broadcastMap(self):
        print("Broadcasting map...")
        [print(f"socket: {socket}") for id, socket in self.sockets.items()]
        for id, websocket in self.sockets.items():
            await websocket.send(self.game.getCurrentMap(self.playerIdDict[id]))

    def _getAvailablePlayerId(self):
        allPlayerIds = list(self.playerIdDict.values())
        [print(f"playerId: {id}") for id in allPlayerIds]

        availablePlayerIds = list(map(lambda x: x + 1, range(10)))
        for playerId in allPlayerIds:
            availablePlayerIds.remove(playerId)

        [print(f"availableId: {id}") for id in availablePlayerIds]
        return availablePlayerIds[0]

    def start(self):
        self.game.start()
        runGameLoop = websockets.serve(
            self._listenForMessages, 'localhost', 9292)

        asyncio.get_event_loop().run_until_complete(runGameLoop)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = Server()
    server.start()
