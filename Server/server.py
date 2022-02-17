import asyncio
import websockets
from game import Game


class Server:
    def __init__(self):
        self.game = Game()

    async def _handleInput(self, websocket, path):
        name = await websocket.recv()
        print("{} has connected.".format(name))

        greeting = "Hello {}! You have successfully connected.".format(name)
        await websocket.send(greeting)

    def start(self):
        runGameLoop = websockets.serve(self._handleInput, 'localhost', 9292)

        asyncio.get_event_loop().run_until_complete(runGameLoop)
        asyncio.get_event_loop().run_forever()


server = Server()
server.start()
