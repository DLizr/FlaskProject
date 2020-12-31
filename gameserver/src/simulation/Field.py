from src.simulation.data.Building import Building
from src.simulation.data.InvalidBuilding import InvalidBuilding


class Field:
    TILE_INVALID = InvalidBuilding()
    
    def __init__(self, base: list, width: int, height: int):
        self.__base = base
        self.__width = width
        self.__height = height
        
        self.__coreCount = 0
    
    def setCoreCount(self, coreCount: int):
        if (self.__coreCount == 0):
            self.__coreCount = coreCount
    
    def noCores(self):
        return self.__coreCount == 0
    
    def breakCore(self):
        self.__coreCount -= 1
    
    def get(self, x: int, y: int) -> Building:
        if (0 <= x < self.__width and 0 <= y < self.__height):
            return self.__base[y * self.__width + x]
        return self.TILE_INVALID
    
    def remove(self, x: int, y: int):
        self.__base[y * self.__width + x] = None
    
    def getWidth(self) -> int:
        return self.__width
    
    def getHeight(self) -> int:
        return self.__height
    
    def __str__(self):
        res = "Field:"
        for i in range(len(self.__base)):
            if (i % self.__width == 0):
                res += "\n\t"
            res += str(self.__base[i]) + "\t"
        
        return res
