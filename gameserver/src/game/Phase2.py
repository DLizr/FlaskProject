import asyncio

from src.player.Player import Player
from src.player.Messages import Messages


class Phase2:

    def __init__(self, player1: Player, player2: Player, base1: list, base2: list):
        self.__player1 = player1
        self.__player2 = player2
        self.__N = 72  # (7+4) * (7+4) - 7*7

        self.__time = 30
        self.__base1 = base1
        self.__base2 = base2
        self.__attackBase1 = []
        self.__attackBase2 = []

    async def start(self):
        await Messages.startPhase2(self.__player1)
        await Messages.startPhase2(self.__player2)

        await self.__sendBases()

        for i in range(self.__time + 1):
            await self.__player1.sendMessage("TIME:{}".format(str(self.__time - i)))
            await self.__player2.sendMessage("TIME:{}".format(str(self.__time - i)))
            await asyncio.sleep(1)

        await self.__getAttackBases()

    async def __sendBases(self):
        await Messages.sendBase(self.__player1)

        for building in self.__base2:
            await self.__player1.sendMessage(building)

        await Messages.sendBase(self.__player2)

        for building in self.__base1:
            await self.__player2.sendMessage(building)

    async def __getAttackBases(self):
        await Messages.getBase(self.__player1)

        for i in range(self.__N):
            for _ in range(2):
                msg = self.__player1.getMessageIfReceived()
                if msg:
                    break

                await self.__player1.ping()
                await asyncio.sleep(1)

            self.__attackBase1.append(msg)

        await Messages.getBase(self.__player2)

        for i in range(self.__N):
            for _ in range(2):
                msg = self.__player2.getMessageIfReceived()
                if msg:
                    break

                await self.__player2.ping()
                await asyncio.sleep(1)

            self.__attackBase2.append(msg)