import asyncio

from websockets.exceptions import ConnectionClosedOK

from src.util.Logger import logger
from src.exceptions.PlayerKickedException import PlayerKickedException
from src.player.Player import Player


class Messages:
    
    @staticmethod
    async def askIfReady(player: Player) -> bool:
        """
        Ready = True, AFK = False.
        """
        player.clearMessages()
        await player.sendMessage("READY_CHECK")
        
        try:
            for _ in range(10):  # A player has 10 seconds to send the ready signal.
                msg = player.getMessageIfReceived()
                if msg == "READY":
                    return True
                await player.ping()
                await asyncio.sleep(1)
        except ConnectionClosedOK as e:
            e.player = player
            raise e
        
        return False
    
    @staticmethod
    async def startPhase1(player: Player):
        
        player.clearMessages()
        await player.sendMessage("PHASE_1")
        
        try:
            for _ in range(5):
                msg = player.getMessageIfReceived()
                if msg == "OK":
                    return
                await player.ping()
                await asyncio.sleep(1)
        except ConnectionClosedOK as e:
            e.player = player
            raise e
        
        logger.error("{} received a PHASE_1 signal but didn't respond!".format(player.getAddress()))
        await player.disconnect()
        raise PlayerKickedException(player, "No response")
    
    @staticmethod
    async def getBase(player: Player):
        
        player.clearMessages()
        await player.sendMessage("GET_BASE")
        try:
            for _ in range(5):
                msg = player.getMessageIfReceived()
                if msg == "OK":
                    return
                await player.ping()
                await asyncio.sleep(1)
        except ConnectionClosedOK as e:
            e.player = player
            raise e
        
        logger.error("{} received a GET_BASE signal but didn't respond!".format(player.getAddress()))
        await player.disconnect()
        raise PlayerKickedException(player, "No response")
