import asyncio

from src.player.Player import Player
from src.player.Messages import Messages


class Phase1:
    
    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2
        
        self.__time = 30
        self.__base1 = None
        self.__base2 = None
    
    async def start(self):
        await Messages.startPhase1(self.__player1)
        await Messages.startPhase1(self.__player2)
        
        for i in range(self.__time):
            await self.__player1.sendMessage("TIME:{}".format(str(self.__time - i)))
            await self.__player2.sendMessage("TIME:{}".format(str(self.__time - i)))
            await asyncio.sleep(1)
