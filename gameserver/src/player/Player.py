import asyncio

import websockets

from src.util.Logger import logger
from src.website import HttpPipe


class Player:
    def __init__(self, websocket: websockets.WebSocketClientProtocol):
        self.__address: str = websocket.remote_address[0] + ":" + str(websocket.remote_address[1])
        self.__websocket = websocket
        
        self.__ID = 0
    
    def getAddress(self) -> str:
        return self.__address
    
    async def sendMessage(self, msg: str):
        try:
            await self.__websocket.send(msg)
        except websockets.exceptions.ConnectionClosed as e:
            e.player = self
            raise e
    
    async def sendMessageSafe(self, msg: str):
        """
        Do not use it if the game is in progress!
        """
        try:
            await self.__websocket.send(msg)
        except websockets.exceptions.ConnectionClosed:
            return
    
    async def disconnect(self):
        HttpPipe.removePlayer(self.__ID)
        try:
            await self.__websocket.ping()
            await self.__websocket.close()
            logger.info(self.__address + " has been disconnected.")
        except websockets.ConnectionClosed:  # Already closed, no need.
            return
    
    def clearMessages(self):
        self.__websocket.messages.clear()
    
    def getMessageIfReceived(self):
        try:
            return self.__websocket.messages.popleft()
        except IndexError:
            return None
    
    async def ping(self):
        try:
            await self.__websocket.ping()
        except websockets.exceptions.ConnectionClosed as e:
            e.player = self
            raise e
    
    def setId(self, ID: int):
        if (self.__ID == 0):
            self.__ID = ID
    
    def getId(self):
        return self.__ID

    def __repr__(self):
        return "Player({}, address={})".format(self.__ID, self.__address)
