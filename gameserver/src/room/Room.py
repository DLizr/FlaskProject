import asyncio

from websockets.exceptions import ConnectionClosed


class Room:
    def __init__(self, size: int):
        self.__players = set()
        self.__size = size
        
        self.__ID: int = None
        self.__started = False
        self.__finished = False
    
    def tryToAddPlayer(self, player) -> bool:
        """
        Returns True if added and False if not.
        """
        if not self.isFull():
            self.__players.add(player)
        else:
            return False
        return True
    
    async def start(self):
        if self.__started:
            await self.__keepConnected()
        self.__started = True
        while True:
            await asyncio.sleep(1)
            for player in self.__players:
                try:
                    await player.sendMessage("Game!")
                except ConnectionClosed:
                    self.__players.remove(player)
                    winner = self.__players.pop()
                    await self.__gameOver(winner, player)
                    return
    
    @staticmethod
    async def __gameOver(winner, loser):
        await winner.sendMessageSafe("You win!")
        await winner.disconnect()  # TODO: congratulate winner.

        await loser.sendMessageSafe("You lose!")
        await loser.disconnect()  # TODO: roast loser.
        
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
