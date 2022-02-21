from enum import Enum
import random
import sys
import os

sys.path.append(sys.path[0] + "/..")

from Shared.models import Position, Player, Entity, Item, Creature, Monster, Bean


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class MapFactory:
    def __init__(self):
        pass

    def makeMap(self, entityDict):
        emptyMap = self._makeEmptyMap()
        for id, entity in entityDict.items():
            row = entity.position.y
            column = entity.position.x
            emptyMap[row][column] = self._getCharacterFromEntity(entity)
        return emptyMap

    def makeMapString(self, entityDict):
        map = self.makeMap(entityDict)
        string = ""
        for row in map:
            string += "|"
            for character in row:
                string += f" {character}"
            string += " |\n"
        return string

    def makeStatsString(self, entityDict, id):
        if entityDict[id] is not None:
            return f"Health: {entityDict[id].health}\nBeans: {entityDict[id].beanCount}"
        return ""

    def _getCharacterFromEntity(self, entity):
        if type(entity) is Player:
            return str(entity.id)
        elif type(entity) is Item:
            return "i"
        elif type(entity) is Monster:
            return "M"
        return "?"

    def _makeEmptyMap(self, emptyCharacter="_"):
        return [[emptyCharacter for x in range(Game.MAP_SIZE)] for y in range(Game.MAP_SIZE)]


class Game:
    MAP_SIZE = 10
    BEAN_DROP_COUNT = 4

    def __init__(self):
        self.entityDict = dict()

    def start(self, entityDict=dict()):
        self.entityDict = entityDict
        self._spawnMonsters(5)

    def getCurrentMap(self, id):
        factory = MapFactory()
        return factory.makeMapString(self.entityDict) + "\n" + factory.makeStatsString(self.entityDict, id)

    def getGlobalMap(self):
        factory = MapFactory()
        return factory.makeMapString(self.entityDict)

    def addNewPlayer(self, id):
        player = Player(id, f"Player {id}", self._getRandomVacantPosition())
        print(f"Adding player {player} with id {id}")
        self.entityDict[id] = player

    def removePlayer(self, id):
        del self.entityDict[id]

    def movePlayer(self, id, direction):
        newPosition = self._getNewPosition(
            self.entityDict[id].position, direction)

        if not self._isPositionInBounds(newPosition):
            return

        entity = self._getEntityAtPosition(newPosition)
        if issubclass(type(entity), Creature) and self.entityDict[id] is not None:
            self._attackCreature(self.entityDict[id], entity)
        else:
            self.entityDict[id].position = newPosition

    def healPlayer(self, id):
        immutableEntity = self.entityDict[id]
        if immutableEntity is not None:
            if immutableEntity.beanCount > 0 and immutableEntity.health <= immutableEntity.maxHealth - Bean.HEALTH:
                self.entityDict[id].health += Bean.HEALTH
                self.entityDict[id].beanCount -= 1

    def _isPositionInBounds(self, position):
        return 0 <= position.x < Game.MAP_SIZE and 0 <= position.y < Game.MAP_SIZE

    def _spawnMonsters(self, count):
        for i in range(count):
            position = self._getRandomVacantPosition()
            self._spawnMonsterAtPosition(position)

    def _spawnMonsterAtPosition(self, position):
        id = random.randint(2000000, 2999999)
        monster = Monster(id, "Goblin", position)
        self.entityDict[id] = monster

    def _attackCreature(self, attackingCreature, attackedCreature):
        if self._isHitSuccessful(attackingCreature.hitChance):
            attackedCreature.health -= 1
            self._evaluateHealth(attackedCreature)

        if self._isHitSuccessful(attackedCreature.hitChance):
            attackingCreature.health -= 1
            self._evaluateHealth(attackingCreature)

    def _evaluateHealth(self, creature):
        if creature.health <= 0:
            previousPosition = creature.position
            creature.position = self._getRandomVacantPosition()
            creature.health = creature.maxHealth
            if type(creature) is Player:
                creature.beanCount = 0
            elif type(creature) is Monster:
                self._distributeBeansAroundPosition(previousPosition)

    def _distributeBeansAroundPosition(self, middlePosition):
        positions = self._getAdjacentPositions(middlePosition)
        for position in positions:
            entity = self._getEntityAtPosition(position)
            if entity is not None and type(entity) is Player:
                self._giveBeansToPlayer(entity)

    def _giveBeansToPlayer(self, player):
        currentBeanCount = self.entityDict[player.id].beanCount
        if currentBeanCount + Game.BEAN_DROP_COUNT > player.maxBeanCount:
            self.entityDict[player.id].beanCount = player.maxBeanCount
        else:
            self.entityDict[player.id].beanCount += Game.BEAN_DROP_COUNT

    def _getAdjacentPositions(self, position):
        return [Position(position.x - 1, position.y),
                Position(position.x, position.y + 1),
                Position(position.x + 1, position.y),
                Position(position.x, position.y - 1)]

    def _isHitSuccessful(self, probability):
        maxValue = int(probability * 100)
        randomInt = random.randint(1, 100)
        return randomInt <= maxValue

    def _isPositionVacant(self, position):
        entity = self._getEntityAtPosition(position)
        if entity is None or entity is Item:
            return True
        return False

    def _getEntityAtPosition(self, position) -> Entity:
        for id, entity in self.entityDict.items():
            if entity.position == position:
                return entity
        return None

    def _getVectorFromDirection(self, direction):
        if direction == Direction.LEFT:
            return Position(-1, 0)
        elif direction == Direction.RIGHT:
            return Position(1, 0)
        elif direction == Direction.UP:
            return Position(0, -1)
        return Position(0, 1)

    def _getNewPosition(self, position, direction):
        vector = self._getVectorFromDirection(direction)
        return Position(position.x + vector.x,
                        position.y + vector.y)

    def _getRandomVacantPosition(self):
        allPositions = self._getAllPositions()
        for id, entity in self.entityDict.items():
            try:
                allPositions[entity.position.y].remove(entity.position)
            except ValueError:
                continue

        maxRow = len(allPositions) - 1
        randomRowIndex = random.randint(0, maxRow)
        maxColumn = len(allPositions[randomRowIndex]) - 1
        randomColumnIndex = random.randint(0, maxColumn)
        return allPositions[randomRowIndex][randomColumnIndex]

    def _getAllPositions(self):
        return [[Position(x, y) for x in range(Game.MAP_SIZE)] for y in range(Game.MAP_SIZE)]


def testGame():
    entities = {1: Player(1, "Jack", maxHealth=20)}
    game = Game()
    game.start(entityDict=entities)
    map = game.getCurrentMap()
    refreshMap(map, game)

    while True:
        key = input("Next move:")
        if key == "w":
            game.movePlayer(1, Direction.UP)
        elif key == "s":
            game.movePlayer(1, Direction.DOWN)
        elif key == "a":
            game.movePlayer(1, Direction.LEFT)
        elif key == "d":
            game.movePlayer(1, Direction.RIGHT)
        elif key == "h":
            game.healPlayer(1)
        elif key == "q":
            break

        map = game.getCurrentMap()
        refreshMap(map, game)


def refreshMap(map, game):
    os.system("clear")
    os.system(f"echo '{map}'")
    os.system(f"echo 'Health: {game.entityDict[1].health}'")
    os.system(f"echo 'Beans: {game.entityDict[1].beanCount}'")


if __name__ == "__main__":
    testGame()
