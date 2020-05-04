import asyncio

from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from src.util.Logger import logger
from src.exceptions.PlayerKickedException import PlayerKickedException
from src.player.Player import Player
from src.game.Game import Game


class Room:
    def __init__(self, size: int):
        self.__players = set()
        self.__size = size
        
        self.__ID: int = None
        self.__started = False
        self.__finished = False
    
    def tryToAddPlayer(self, player: Player) -> bool:
        """
        Returns True if added and False if not.
        """
        if not self.isFull():
            logger.debug("Adding {} to room {}.".format(player.getAddress(), str(self.__ID)))
            self.__players.add(player)
        else:
            return False
        return True
    
    async def connectPlayer(self, player: Player):
        while len(self.__players) < 2:
            await asyncio.sleep(1)
            try:
                await player.ping()
            except ConnectionClosedOK:
                logger.info("{} has disconnected.".format(player.getAddress()))
                return
            except ConnectionClosedError as e:
                logger.error("{}: Connection with {} has been terminated. Reason: {}".format(e.code, player.getAddress(), e.reason))
                return
        await self.__start()
    
    async def __start(self):
        
        if self.__started:                # Player 1 comes here and starts the game,
            await self.__keepConnected()  # Player 2 goes to __keepConnected() to avoid doing all the tasks twice.
        self.__started = True
        logger.info("The game in room #{} has started.".format(str(self.__ID)))
        
        player1, player2 = self.__players
        game = Game(self.__ID)
        
        try:
            await game.start(player1, player2)
        except ConnectionClosedOK as e:
            logger.info("{} has disconnected.".format(e.player.getAddress()))
            await self.__onConnectionClose(e.player)  # Ignore these errors.
        except PlayerKickedException as e:
            logger.info("{} has been kicked. Reason: {}.".format(e.player.getAddress(), e.reason))
            await self.__onConnectionClose(e.player)
        except ConnectionClosedError as e:
            logger.error("{}: Connection with {} has beed terminated. Reason: {}".format(e.code, e.player, e.reason))  # Ignore this error.
            await self.__onConnectionError()
        
        winner = game.getWinner()
        if (winner == 1):
            await self.__gameOver(player1, player2)
        elif (winner == 2):
            await self.__gameOver(player2, player1)
        elif (winner == 3):
            await self.__onDraw()
        else:
            await self.__onConnectionError()  # Theoretically it will never happen.
    
    async def __onConnectionClose(self, player: Player):
        self.__players.remove(player)
        winner = self.__players.pop()
        await self.__gameOver(winner, player)
        return

    async def __onConnectionError(self):
        for player in self.__players:
            await player.disconnect()
    
    @staticmethod
    async def __gameOver(winner: Player, loser: Player):
        await winner.disconnect()  # TODO: congratulate winner.
        await loser.disconnect()  # TODO: roast loser.
    
    async def __onDraw(self):
        for player in self.__players:
            await player.disconnect()
        
    async def __keepConnected(self):
        while not self.__finished:
            await asyncio.sleep(2)
    
    def isFull(self) -> bool:
        return len(self.__players) == self.__size
    
    def setID(self, ID: int):
        if self.__ID is None:
            self.__ID = ID
    
    def getID(self):
        return self.__ID
    
    def __repr__(self):
        return "Room({}, started={}, finished={})".format(self.__players, self.__started, self.__finished)
