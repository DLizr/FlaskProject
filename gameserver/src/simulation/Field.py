class Field:
    
    def __init__(self, base: list, width: int, height: int):
        self.__base = base
        self.__width = width
        self.__height = height
    
    def get(self, x: int, y: int):
        if (0 <= x < self.__width and 0 <= y < self.__height):
            return self.__base[y * self.__width + x]
        return None
    
    def __str__(self):
        res = "Field:"
        for i in range(len(self.__base)):
            if (i % self.__width == 0):
                res += "\n\t"
            res += str(self.__base[i]) + "\t"
        
        return res
