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
        self.__winner = 0
    
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
        
        self.__getWinner(s1, s2)
    
    def __getWinner(self, s1: Simulator, s2: Simulator):
        """
        Winner is the player who either won in both rounds 
        or won in a shorter time than his opponent.
        """
        w1, w2 = s1.getWinner(), s2.getWinner()
        
        if (w1 == w2):
            self.__winner = w1
            return
        
        if (w1 == 1):
            victoryTime1 = s1.getTime()
            victoryTime2 = s2.getTime()
        else:
            victoryTime2 = s1.getTime()
            victoryTime1 = s2.getTime()
        
        if (victoryTime1 < victoryTime2):
            self.__winner = 1
        elif (victoryTime1 > victoryTime2):
            self.__winner = 2
        else:
            self.__winner = 3
    
    async def __sendBase(self, base):
        await Messages.sendBase(self.__player1)
        await Messages.sendBase(self.__player2)

        for building in base:
            await self.__player1.sendMessage(building)
            await self.__player2.sendMessage(building)
    
    def getWinner(self):
        return self.__winner
