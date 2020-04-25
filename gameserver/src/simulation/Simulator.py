from src.simulation.Field import Field

from src.simulation.data.Wall import Wall
from src.simulation.data.Core import Core
from src.simulation.data.Cannon import Cannon


class Simulator:
    
    def __init__(self, base: list):
        self.__base: Field = None
        self.__observers = set()
        
        self.__parseBase(base)
    
    def __parseBase(self, base):
        field = []
        for i, cell in enumerate(base):
            if (cell == "0"):
                field.append(None)
            elif (cell == "W"):
                field.append(Wall())
            elif (cell == "C"):
                field.append(Core())
            elif (cell == "A"):
                c = Cannon(i % 7, i // 7)
                field.append(c)
                self.__observers.add(c)
        
        self.__base = Field(field, 7, 7)
        
        for observer in self.__observers:
            observer.setField(self.__base)
    
    def update(self):
        for observer in self.__observers:
            observer.update()
