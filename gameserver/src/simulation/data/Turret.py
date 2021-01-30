from collections import deque
import random

from src.simulation.data._InteractingBuilding import InteractingBuilding
from src.simulation.Field import Field
from src.util.pathfinding.SearchInCross import SearchInCross


class Turret(InteractingBuilding):
    hp = 10
    reloadSpeed = 1
    damage = 2
    speed = 2

    def __init__(self, x: int, y: int):
        super().__init__(self.hp, x, y)
        self.__lastTarget: tuple = None
        self.__x = x
        self.__y = y
        self.__field = None

        self.__noTargets = False
        self.__reload = 0
        self.__hitQueue = []
        self.__targetFinder: SearchInCross = None

    # Override
    def setField(self, field: Field):
        self.__field = field
        self.__targetFinder = SearchInCross(field, self.__x, self.__y)
        self.__targetFinder.setCellValidator(self.__isCellValid)
        self.__targetFinder.setAttackingFunction(self.__canAttack)
        self.__targetFinder.findTargets()
        pass

    # Override
    def update(self):
        if (self.getHP() <= 0):
            return
        self.__handleQueue()
        if (self.__noTargets):
            return
        if (not (self.__lastTarget and self.__field.get(*self.__lastTarget))):
            self.__findTarget()
            if (not self.__lastTarget or not self.__field.get(*self.__lastTarget)):
                self.__noTargets = True
                return
        self.__shoot()

        if (self.__reload == 0):  # Just shot
            return "S:{}:{}:{}:{}".format(str(self.__x), str(self.__y), str(self.__lastTarget[0]),
                                          str(self.__lastTarget[1]))

    def __findTarget(self):
        target = self.__targetFinder.getNextTarget()
        if (target):
            self.__lastTarget = target

    def __isCellValid(self, x: int, y: int) -> bool:
        c = self.__field.get(x, y)
        return c != Field.TILE_INVALID

    def __canAttack(self, x: int, y: int) -> bool:
        if x != self.__x and y != self.__y:
            return False
        c = self.__field.get(x, y)
        return c and c.getTeam() == self.ATTACKING

    def __shoot(self):
        if (self.__reloading()):
            return

        targetX, targetY = self.__lastTarget
        distance = ((targetX - self.__x) ** 2 + (targetY - self.__y) ** 2) ** 0.5
        time = distance // self.speed

        self.__hitQueue.append([self.__lastTarget, time])

    def __reloading(self):
        self.__reload += 1

        if (self.__reload == self.reloadSpeed):
            self.__reload = 0
            return False

        return True

    def __handleQueue(self):
        for i in range(len(self.__hitQueue)):
            coords = self.__hitQueue[i][0]
            self.__hitQueue[i][1] -= 1

            if (self.__hitQueue[i][1] <= 0):
                self.__hit(coords)
                self.__hitQueue.pop(i)
                break

    def __hit(self, coords):
        target = self.__field.get(*coords)
        if (not target):
            return
        target.dealDamage(self.damage)

    def hasTarget(self):
        return not self.__noTargets or self.__hitQueue

    # Override
    def getTeam(self):
        return self.DEFENDING
