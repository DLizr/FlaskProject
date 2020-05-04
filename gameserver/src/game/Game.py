import asyncio

from src.util.Logger import logger

from src.exceptions.PlayerKickedException import PlayerKickedException

from src.player.Messages import Messages
from src.player.Player import Player

from src.game.Phase1 import Phase1
from src.game.Phase2 import Phase2
from src.game.Phase3 import Phase3


class Game:

    def __init__(self, ID: int):
        self.__ID = ID
        
        self.__winner = 0

    async def start(self, player1: Player, player2: Player):
        if not await Messages.askIfReady(player1):
            await player1.sendMessageSafe("KICKED:AFK")
            await player1.disconnect()
            raise PlayerKickedException(player1, "Not ready for battle")
        
        if not await Messages.askIfReady(player2):
            await player2.sendMessageSafe("KICKED:AFK")
            await player2.disconnect()
            raise PlayerKickedException(player2, "Not ready for battle")
        
        p1 = Phase1(player1, player2)
        logger.debug("Game #{}: phase 1 begins.".format(self.__ID))
        await p1.start()
        
        base1 = p1.getPlayer1Base()
        base2 = p1.getPlayer2Base()
        
        p2 = Phase2(player1, player2, base1, base2)
        logger.debug("Game #{}: phase 2 begins.".format(self.__ID))
        await p2.start()
        
        attackBase1 = p2.getAttackBase1()
        attackBase2 = p2.getAttackBase2()
        
        finalBase1 = self.__mergeBase(attackBase2, base1)
        finalBase2 = self.__mergeBase(attackBase1, base2)
        
        p3 = Phase3(player1, player2, finalBase1, finalBase2)
        logger.debug("Game #{}: phase 3 begins.".format(self.__ID))
        await p3.start()
        
        self.__winner = p3.getWinner()
        
    @staticmethod
    def __mergeBase(attack: list, defend: list):
        final = []
        for i in range(121):
            if (i < 22 or i > 98):
                final.append(attack.pop(0))
            elif (i % 11 < 2 or i % 11 > 8):
                final.append(attack.pop(0))
            else:
                final.append(defend.pop(0))
        
        return final
    
    def getWinner(self):
        return self.__winner
