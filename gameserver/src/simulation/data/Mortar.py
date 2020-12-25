from collections import deque
import random

from src.simulation.data._InteractingBuilding import InteractingBuilding
from src.simulation.Field import Field


class Mortar(InteractingBuilding):
    
    __hp = 10
    __reloadSpeed = 8
    __damage = 15
    __speed = 0.125
    
    def __init__(self, x: int, y: int):
        self.__lastTarget: tuple = None
        self.__x = x
        self.__y = y
        self.__field = None
        
        self.__noTargets = False
        self.__reload = random.randint(0, 7)
        self.__hitQueue = []
    
    def getHP(self):
        return self.__hp
    
    def dealDamage(self, dmg: int):
        self.__hp -= dmg
    
    def setField(self, field: Field):
        self.__field = field
    
    def update(self):
        if (self.__hp <= 0):
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
            return "S:{}:{}:{}:{}".format(str(self.__x), str(self.__y), str(self.__lastTarget[0]), str(self.__lastTarget[1]))

    
    def __findTarget(self):
        x, y = self.__x, self.__y

        distance = [[0 for j in range(max(0, x - 9), x + 10)] for i in range(max(0, y - 9), y + 10)]
        bfsQueue = deque()
        bfsQueue.appendleft((x, y))
        while (len(bfsQueue) > 0):
            tileX, tileY = bfsQueue.pop()
            if (distance[tileY][tileX] > 9):
                break
            if (self.__tryToAttack(tileX, tileY)):
                break
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (self.__checkCell(tileX + dx, tileY + dy)):
                    if (distance[tileY + dy][tileX + dx] == 0):
                        distance[tileY + dy][tileX + dx] = distance[tileY][tileX] + 1
                        bfsQueue.appendleft((tileX + dx, tileY + dy))
            
    
    def __checkCell(self, x: int, y: int) -> bool:
        c = self.__field.get(x, y)
        return c != Field.TILE_INVALID
    
    def __tryToAttack(self, x: int, y: int) -> bool:
        c = self.__field.get(x, y)
        if (c and c.getTeam() == self.ATTACKING):
            self.__lastTarget = (x, y)
            return True
        
        return False
    
    def __shoot(self):
        if (self.__reloading()):
            return
        
        targetX, targetY = self.__lastTarget
        distance = ((targetX - self.__x) ** 2 + (targetY - self.__y) ** 2) ** 0.5
        time = distance // self.__speed
        
        self.__hitQueue.append([self.__lastTarget, time])
            
    def __reloading(self):
        self.__reload += 1
        
        if (self.__reload == self.__reloadSpeed):
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
        target.dealDamage(self.__damage)
        
        if (target.getHP() <= 0):
            self.__field.remove(*self.__lastTarget)
            if (target.__class__.__name__ == "Core"):
                self.__field.breakCore()
    
    def hasTarget(self):
        return not self.__noTargets or self.__hitQueue
    
    def getTeam(self):
        return self.DEFENDING
