import json

class Message:
    def __init__(self, source, action, body = {}):
        self.source = source
        self.action = action
        self.body = body
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
class ClientMessage(Message):
    def __init__(self, action, body = {}):
        super().__init__("client", action, body)
    
class ServerMessage(Message):
    def __init__(self, action, body = {}):
        super().__init__("server", action, body)
    
class MoveMessage(ClientMessage):
    def __init__(self, direction):
        self.direction = direction
        super().__init__('move', { 'direction': direction })

class UseBeanMessage(ClientMessage):
    def __init__(self):
        super().__init__('heal')

class ClientSetNameMessage(ClientMessage):
    def __init__(self, name):
        super().__init__('set_name', { 'name': name})
 
msg = ClientSetNameMessage('micah')
print(msg.toJSON())

# msg = UseBeanMessage()
# print(msg.toJSON())

# msg = MoveMessage('left')
# print(msg.toJSON())

# moveLeftMessage = MoveMessage('left')
# print(moveLeftMessage.toJSON())