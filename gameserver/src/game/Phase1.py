import asyncio

from src.util.Logger import logger
from src.player.Player import Player
from src.player.Messages import Messages
from src.exceptions.PlayerKickedException import PlayerKickedException


class Phase1:

    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2
        self.__M = 7
        self.__N = 7

        self.__time = 30
        self.__base1 = []
        self.__base2 = []

    async def start(self):
        await Messages.startPhase1(self.__player1)
        await Messages.startPhase1(self.__player2)

        for i in range(self.__time + 1):
            await self.__player1.sendMessage("TIME:{}".format(str(self.__time - i)))
            await self.__player2.sendMessage("TIME:{}".format(str(self.__time - i)))
            await asyncio.sleep(1)

        await self.__getBases()

    async def __getBases(self):
        await Messages.getBase(self.__player1)

        for i in range(self.__M * self.__N):
            for _ in range(2):
                msg = self.__player1.getMessageIfReceived()
                if msg:
                    break

                await self.__player1.ping()
                await asyncio.sleep(1)
            else:
                await self.__kick(self.__player1)

            self.__base1.append(msg)

        await Messages.getBase(self.__player2)

        for i in range(self.__M * self.__N):
            for _ in range(2):
                msg = self.__player2.getMessageIfReceived()
                if msg:
                    break

                await self.__player2.ping()
                await asyncio.sleep(1)
            else:
                await self.__kick(self.__player2)

            self.__base2.append(msg)
    
    @staticmethod
    async def __kick(player):
        logger.error("{} stopped responding during base getting!".format(player.getAddress()))
        await player.sendMessageSafe("KICKED:NO_RESPONSE")
        await player.disconnect()
        raise PlayerKickedException(player, "No response")

    def getPlayer1Base(self):
        return self.__base1

    def getPlayer2Base(self):
        return self.__base2
