from src.simulation.data._InteractingBuilding import InteractingBuilding
from src.simulation.Field import Field


class Cannon(InteractingBuilding):
    
    __hp = 10
    __reloadSpeed = 5
    __damage = 5
    
    def __init__(self, x: int, y: int):
        self.__lastTarget: tuple = None
        self.__x = x
        self.__y = y
        self.__field = None
        
        self.__noTargets = False
        self.__reload = 0
    
    def getHP(self):
        return self.__hp
    
    def dealDamage(self, dmg: int):
        self.__hp -= dmg
    
    def setField(self, field: Field):
        self.__field = field
    
    def update(self):
        if (self.__noTargets):
            return
        if (self.__lastTarget and self.__field.get(*self.__lastTarget)):
            self.__shoot()
            return
        
        self.__findTarget()
        if (not self.__lastTarget or not self.__field.get(*self.__lastTarget)):
            self.__noTargets = True
            return
        
        self.__shoot()
    
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
                if (self.__checkCell(x + i2, x + i - i2)):
                    return
                
            for i2 in range(i//2 + 1, i):
                if (self.__checkCell(x + i2 - i, y - i2)):
                    return
                if (self.__checkCell(x + i - i2, y + i2)):
                    return
                if (self.__checkCell(x + i2, y + i2 - i)):
                    return
                if (self.__checkCell(x - i2, x + i - i2)):
                    return
                
                if (self.__checkCell(x + i2 - i, y + i2)):
                    return
                if (self.__checkCell(x + i - i2, y - i2)):
                    return
                if (self.__checkCell(x - i2, y + i2 - i)):
                    return
                if (self.__checkCell(x + i2, x + i - i2)):
                    return
                
            if (self.__checkCell(x, 0)):
                return
            if (self.__checkCell(-x, 0)):
                return
            if (self.__checkCell(0, -y)):
                return
            if (self.__checkCell(0, y)):
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
        target = self.__field.get(*self.__lastTarget)
        target.dealDamage(self.__damage)
        if (target.getHP() <= 0):
            self.__field.remove(*self.__lastTarget)
    
    def __reloading(self):
        if (self.__reload == self.__reloadSpeed):
            self.__reload = 0
            return False
        self.__reload += 1
        return True
    
    def getTeam(self):
        return self.ATTACKING
