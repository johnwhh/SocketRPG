class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Entity:
    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position


class Creature(Entity):
    def __init__(self, id, name, hitChance, maxHealth):
        super().__init__(id, name)
        self.hitChance = hitChance
        self.maxHealth = maxHealth
        self.health = maxHealth


class Player(Creature):
    def __init__(self, id, name, hitChance=0.6, maxHealth=5, maxBeanCount=10):
        super().__init__(id, name, hitChance, maxHealth)
        self.hitChance = hitChance
        self.maxBeanCount = maxBeanCount
        self.beanCount = 0


class Monster(Creature):
    def __init__(self, id, name, hitChance=0.75, maxHealth=5):
        super().__init__(id, name, hitChance, maxHealth)
        self.hitChance = hitChance


class Item(Entity):
    def __init__(self, id, name, position, weight):
        super().__init__(id, name, position)
        self.weight = weight


class Bean(Item):
    def __init__(self, id, name, position):
        super().__init__(id, name, position, 1)
