import json

moveLeftMessageString = """
{ 
    "source": "client",
    "action": "move",
    "body": {
        "direction": "left"
    }
}
"""

beanUserMessageString = """
{ 
    "source": "client",
    "action": "use_item",
    "body": {
        "item_id": 1
    } 
}"""

class UserMoveHandler():
    def execute(self, jsonObject):
        objectBody = jsonObject['body']
        print(objectBody['direction'])

class UserUseItemHandler():
    def execute(self, jsonObject):
        objectBody = jsonObject['body']
        print(objectBody['item_id'])

class ServerMessageHandler:
    def __init__(self):
        self.methods = {
        "move": UserMoveHandler(),
        "use_item": UserUseItemHandler(),
    }

    def execute(self, jsonString):
        jsonObject = json.loads(jsonString)
        try:
            if (jsonObject['source'] != 'client'):
                raise('Cannot accept non client messages')
            jsonAction = jsonObject['action']
            methodHandler = self.methods[jsonAction]
            methodHandler.execute(jsonObject)
        except:
            print('there was an error parsing the message')

serverMessageHandler = ServerMessageHandler()

print(moveLeftMessageString)

serverMessageHandler.execute(moveLeftMessageString)
serverMessageHandler.execute(beanUserMessageString)