import asyncio
import websockets

class Server:
  async def handler(self, websocket, path):
    name = await websocket.recv()
    print("{} has connected.".format(name))

    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)

  async def start(self):
    runGameLoop = websockets.serve(self.handler, 'localhost', 9292)

    asyncio.get_event_loop().run_until_complete(runGameLoop)
    asyncio.get_event_loop().run_forever()

server = Server()
server.start()