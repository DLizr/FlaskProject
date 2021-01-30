import asyncio
import datetime

from src.player.Player import Player

from src.simulation.Field import Field

from src.simulation.data.Wall import Wall
from src.simulation.data.Core import Core
from src.simulation.data.Cannon import Cannon
from src.simulation.data.Mortar import Mortar
from src.simulation.data.Crossbow import Crossbow
from src.simulation.data.Turret import Turret


class Simulator:
    
    def __init__(self, base: list, player: int):
        self.__base: Field = None
        self.__player = player
        
        self.__observers = []
        self.__time = 0
        self.__winner = 0
        
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
                self.__observers.append(c)
            elif (cell == "M"):
                m = Mortar(i % 11, i // 11)
                field.append(m)
                self.__observers.append(m)
            elif (cell == "T"):
                t = Turret(i % 11, i // 11)
                field.append(t)
                self.__observers.append(t)
            elif (cell == "R"):
                c = Crossbow(i % 11, i // 11)
                field.append(c)
                self.__observers.append(c)
        
        self.__base = Field(field, 11, 11)
        self.__base.setCoreCount(cores)
        
        for observer in self.__observers:
            observer.setField(self.__base)
    
    async def startSimulating(self, player1: Player, player2: Player):
        while True:
            startTime = datetime.datetime.now();
            messages = self.__update()
            for msg in messages:
                await player1.sendMessage(msg)
                await player2.sendMessage(msg)
            
            if (self.__base.noCores()):
                if (self.__player == 1):
                    await self.__gameOver(player2, player1)
                    self.__winner = 2
                else:
                    await self.__gameOver(player1, player2)
                    self.__winner = 1
                break
            
            if (self.__noObservers()):
                if (self.__player == 1):
                    await self.__gameOver(player1, player2)
                    self.__winner = 1
                else:
                    await self.__gameOver(player2, player1)
                    self.__winner = 2
                break
            
            timeDelta = datetime.datetime.now() - startTime
            if (timeDelta.seconds < 1 and timeDelta.microseconds <= 250000):
                await asyncio.sleep(0.25 - timeDelta.microseconds / 1000000)
            self.__time += 1
            
    
    def __update(self):
        messages = set()
        for observer in self.__observers:
            msg = observer.update()
            if msg:
                messages.add(msg)
        return messages
    
    def __noObservers(self):
        for observer in self.__observers:
            if (observer.getHP() <= 0):
                self.__observers.remove(observer)
            elif (observer.hasTarget()):
                return False
        return True
    
    async def __gameOver(self, winner: Player, loser: Player):
        await loser.sendMessage("L:{}".format(str(self.__time // 4)))
        await winner.sendMessage("W:{}".format(str(self.__time // 4)))
    
    def getTime(self):
        return self.__time // 4
    
    def getWinner(self):
        return self.__winner
