import asyncio

from src.player.Player import Player

from src.simulation.Field import Field

from src.simulation.data.Wall import Wall
from src.simulation.data.Core import Core
from src.simulation.data.Cannon import Cannon


class Simulator:
    
    def __init__(self, base: list, player: int):
        self.__base: Field = None
        self.__player = player
        
        self.__observers = set()
        self.__time = 0
        
        self.__parseBase(base)
    
    def __parseBase(self, base):
        field = []
        cores = 0
        for i, cell in enumerate(base):
            if (cell == "0"):
                field.append(None)
            elif (cell == "W"):
                field.append(Wall())
            elif (cell == "C"):
                field.append(Core())
                cores += 1
            elif (cell == "A"):
                c = Cannon(i % 11, i // 11)
                field.append(c)
                self.__observers.add(c)
        
        self.__base = Field(field, 11, 11)
        self.__base.setCoreCount(cores)
        
        for observer in self.__observers:
            observer.setField(self.__base)
    
    async def startSimulating(self, player1: Player, player2: Player):
        while True:
            messages = self.__update()
            for msg in messages:
                await player1.sendMessage(msg)
                await player2.sendMessage(msg)
            
            if (self.__base.noCores()):
                winner = abs(self.__player - 3)
                s = self.__time // 4
                await player1.sendMessage("W:{}:{}".format(str(winner), str(s)))
                await player2.sendMessage("W:{}:{}".format(str(winner), str(s)))
                break
            
            await asyncio.sleep(0.25)
            self.__time += 1
            
    
    def __update(self):
        messages = set()
        for observer in self.__observers:
            msg = observer.update()
            if msg:
                messages.add(msg)
        return messages
    
    def getTime(self):
        return self.__time
