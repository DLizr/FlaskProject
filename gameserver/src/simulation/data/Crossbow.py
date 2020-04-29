from src.simulation.data._InteractingBuilding import InteractingBuilding
from src.simulation.Field import Field


class Crossbow(InteractingBuilding):
    
    __hp = 10
    __reloadSpeed = 1
    __damage = 2
    __speed = 0.4
    
    def __init__(self, x: int, y: int):
        self.__lastTarget: tuple = None
        self.__x = x
        self.__y = y
        self.__field = None
        
        self.__noTargets = False
        self.__reload = 0
        self.__hitQueue = []
        self.__direction = [0, 0]
        
        self.__getDirection()
    
    def __getDirection(self):
        if (self.__x < 2):
            self.__direction = [1, 0]
        elif (self.__x > 8):
            self.__direction = [-1, 0]
        elif (self.__y < 2):
            self.__direction = [0, 1]
        elif (self.__y > 8):
            self.__direction = [0, -1]
    
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
        for i in range(1, 11):  # Breadth-first search optimized for finding the closest target first, holy boilerplate.
            if (self.__checkCell(x + i * self.__direction[0], y + i * self.__direction[1])):
                break
    
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
