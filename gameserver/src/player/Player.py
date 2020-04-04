import asyncio

import websockets

from src.room.Room import Room
from src.util.Logger import logger


class Player:
    def __init__(self, ID: int, websocket: websockets.WebSocketClientProtocol):
        self.__ID = ID
        self.__address: str = websocket.remote_address[0] + ":" + str(websocket.remote_address[1])
        self.__websocket = websocket
        
        self.__room: Room = None
    
    def getAddress(self) -> str:
        return self.__address
    
    async def sendMessage(self, msg: str):
        await self.__websocket.send(msg)
    
    async def sendMessageSafe(self, msg: str):
        """
        Do not use it if the game is in progress!
        """
        try:
            await self.__websocket.send(msg)
        except websockets.exceptions.ConnectionClosed:
            return
    
    async def joinTheRoom(self):
        while not self.__room.isFull():
            await asyncio.sleep(1)
            await self.__websocket.send("Ping!")
        await self.__room.start()
    
    def setRoom(self, room: Room):
        if self.__room is None:
            self.__room = room
    
    async def disconnect(self):
        try:
            await self.__websocket.ping()
            await self.__websocket.close()
            logger.info(self.__address + " has been disconnected.")
        except websockets.ConnectionClosed:  # Already closed, no need.
            return
    
    def __repr__(self):
        return "Player({}, address={})".format(self.__ID, self.__address)
