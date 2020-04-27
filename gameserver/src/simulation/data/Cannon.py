import random

from src.simulation.data._InteractingBuilding import InteractingBuilding
from src.simulation.Field import Field


class Cannon(InteractingBuilding):
    
    __hp = 10
    __reloadSpeed = 5
    __damage = 5
    __speed = 0.2
    
    def __init__(self, x: int, y: int):
        self.__lastTarget: tuple = None
        self.__x = x
        self.__y = y
        self.__field = None
        
        self.__noTargets = False
        self.__reload = random.randint(0, 4)
        self.__hitQueue = []
    
    def getHP(self):
        return self.__hp
    
    def dealDamage(self, dmg: int):
        self.__hp -= dmg
    
    def setField(self, field: Field):
        self.__field = field
    
    def update(self):
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
        for i in range(1, 6):  # Breadth-first search optimized for finding the closest target first, holy boilerplate.
            if (i % 2 == 0):
                i2 = i // 2
                if (self.__checkCell(x + i2 - i, y + i2)):
                    return
                if (self.__checkCell(x + i - i2, y - i2)):
                    return
                if (self.__checkCell(x - i2, y + i2 - i)):
                    return
                if (self.__checkCell(x + i2, y + i - i2)):
                    return
                
            for i2 in range(i//2 + 1, i):
                if (self.__checkCell(x + i2 - i, y - i2)):
                    return
                if (self.__checkCell(x + i - i2, y + i2)):
                    return
                if (self.__checkCell(x + i2, y + i2 - i)):
                    return
                if (self.__checkCell(x - i2, y + i - i2)):
                    return
                
                if (self.__checkCell(x + i2 - i, y + i2)):
                    return
                if (self.__checkCell(x + i - i2, y - i2)):
                    return
                if (self.__checkCell(x - i2, y + i2 - i)):
                    return
                if (self.__checkCell(x + i2, y + i - i2)):
                    return
                
            if (self.__checkCell(x - i, y)):
                return
            if (self.__checkCell(x + i, y)):
                return
            if (self.__checkCell(x, y - i)):
                return
            if (self.__checkCell(x, y + i)):
                return
    
    def __checkCell(self, x: int, y: int):
        c = self.__field.get(x, y)
        
        if (c and c.getTeam() == self.DEFENDING):
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
        return self.ATTACKING
