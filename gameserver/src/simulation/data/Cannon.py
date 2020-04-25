from src.simulation.data._InteractingBuilding import InteractingBuilding
from src.simulation.Field import Field


class Cannon(InteractingBuilding):
    
    __hp = 10
    
    def __init__(self, x: int, y: int):
        self.__lastTarget: tuple = None
        self.__x = x
        self.__y = y
        self.__field = None
    
    def getHP(self):
        return self.__hp
    
    def onDamageReceived(self, dmg: int):
        self.__hp -= dmg
    
    def setField(self, field: Field):
        self.__field = field
    
    def update(self):
        if (self.__lastTarget and self.__field[self.__lastTarget]):
            return  # Shoot it.
        
        self.__findTarget()
        print(self.__lastTarget)
    
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
    
    def getTeam(self):
        return self.ATTACKING
