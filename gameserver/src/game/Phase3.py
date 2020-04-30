import asyncio

from src.player.Messages import Messages
from src.player.Player import Player

from src.simulation.Simulator import Simulator


class Phase3:
    
    def __init__(self, player1: Player, player2: Player, base1: list, base2: list):
        self.__player1 = player1
        self.__player2 = player2
        
        self.__base1 = base1
        self.__base2 = base2
        
        self.__time = 120
    
    async def start(self):
        await Messages.startPhase3(self.__player1)
        await Messages.startPhase3(self.__player2)
        
        await self.__sendBase(self.__base1)
        
        s1 = Simulator(self.__base1, 1)
        await s1.startSimulating(self.__player1, self.__player2)
        await asyncio.sleep(5)
        
        await self.__sendBase(self.__base2)
        
        s2 = Simulator(self.__base2, 2)
        await s2.startSimulating(self.__player1, self.__player2)
        await asyncio.sleep(5)
        
        t1 = s1.getTime()
        t2 = s2.getTime()
        
        msg1 = "R:"
        msg2 = "R:"
        
        if (s1.getWinner() == 1):
            msg1 += "W:{}:".format(t1)
        else:
            msg1 += "L:{}:".format(t1)
        
        if (s2.getWinner() == 2):
            msg2 += "W:{}:".format(t2)
            msg1 += "L:{}".format(t2)
        else:
            msg2 += "L:{}:".format(t2)
            msg1 += "W:{}".format(t2)

        if (s1.getWinner() == 2):
            msg2 += "W:{}".format(t1)
        else:
            msg2 += "L:{}".format(t1)
        
        await self.__player1.sendMessage(msg1)
        await self.__player2.sendMessage(msg2)
    
    async def __sendBase(self, base):
        await Messages.sendBase(self.__player1)
        await Messages.sendBase(self.__player2)

        for building in base:
            await self.__player1.sendMessage(building)
            await self.__player2.sendMessage(building)