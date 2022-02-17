class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Position({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def zero():
        return Position(0, 0)

class Entity:
    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position

    def __str__(self) -> str:
        return f"Entity({self.id}, {self.name}, {self.position})"


class Creature(Entity):
    def __init__(self, id, name, position, hitChance, maxHealth):
        super().__init__(id, name, position)
        self.hitChance = hitChance
        self.maxHealth = maxHealth
        self.health = maxHealth


class Player(Creature):
    def __init__(self, id, name, position=Position.zero(), hitChance=0.6, maxHealth=5, maxBeanCount=10):
        super().__init__(id, name, position, hitChance, maxHealth)
        self.hitChance = hitChance
        self.maxBeanCount = maxBeanCount
        self.beanCount = 0


class Monster(Creature):
    def __init__(self, id, name, position=Position.zero(), hitChance=0.75, maxHealth=5):
        super().__init__(id, name, position, hitChance, maxHealth)
        self.hitChance = hitChance


class Item(Entity):
    def __init__(self, id, name, position, weight):
        super().__init__(id, name, position)
        self.weight = weight


class Bean(Item):
    HEALTH = 1

    def __init__(self, id, name, position):
        super().__init__(id, name, position, 1)
