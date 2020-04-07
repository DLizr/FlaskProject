import asyncio

from src.player.Player import Player
from src.player.Messages import Messages


class Phase1:

    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2
        self.__M = 10
        self.__N = 10

        self.__time = 30
        self.__base1 = [[None for _ in range(self.__N)] for _ in range(self.__M)]
        self.__base2 = [[None for _ in range(self.__N)] for _ in range(self.__M)]

    async def start(self):
        await Messages.startPhase1(self.__player1)
        await Messages.startPhase1(self.__player2)

        for i in range(self.__time):
            await self.__player1.sendMessage("TIME:{}".format(str(self.__time - i)))
            await self.__player2.sendMessage("TIME:{}".format(str(self.__time - i)))
            await asyncio.sleep(1)
        
        self.__getBases()

    async def __getBases(self):
        Messages.getBase(self.__player1)
        
        for i in range(self.__M * self.__N):
            for _ in range(2):
                msg = self.__player1.getMessageIfReceived()
                if msg:
                    break
                
                await self.__player1.ping()
                await asyncio.sleep(1)
                
            self.__base1[i//self.__M][i%self.__M] = msg
            
            
        Messages.getBase(self.__player2)
        
        for i in range(self.__M * self.__N):
            for _ in range(2):
                msg = self.__player2.getMessageIfReceived()
                if msg:
                    break
                
                await self.__player2.ping()
                await asyncio.sleep(1)
                
            self.__base2[i//self.__M][i%self.__M] = msg
