from src.simulation.data.Wall import Wall
from src.simulation.data.Core import Core
from src.simulation.data.Cannon import Cannon


class Simulator:
    
    def __init__(self, base: list):
        self.__base = []
        self.__observers = set()
        
        self.__parseBase(base)
    
    def __parseBase(self, base):
        for cell in base:
            if (cell == "0"):
                self.__base.append(None)
            elif (cell == "W"):
                self.__base.append(Wall())
            elif (cell == "C"):
                self.__base.append(Core())
            elif (cell == "A"):
                c = Cannon()
                self.__base.append(c)
                self.__observers.add(c)
        
        print(self.__base)


s = Simulator(["W", "C", "W", "C", "0", "0", "0", "0"])
