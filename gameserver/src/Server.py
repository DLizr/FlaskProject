import asyncio

import websockets

from src.util.Logger import logger
from src.room.RoomList import RoomList
from src.player.Player import Player


class Server:
    __ID = 0
    __cooldown = 0
    
    @classmethod
    async def userHandler(cls, websocket: websockets.WebSocketClientProtocol, _):  # _ is path.
        player = Player(cls.__ID, websocket)
        
        cls.__cooldown += 4
        await asyncio.sleep(cls.__cooldown)  # Players can join once per 4 seconds.
        cls.__cooldown -= 4
        
        cls.__ID += 1
        logger.info(player.getAddress() + " has connected.")
        
        room = RoomList.addPlayer(player)
        await room.connectPlayer(player)
        
        RoomList.removeRoom(room.getID())
        logger.info("The game in room #{} is over.".format(room.getID()))
    
    @classmethod
    def run(cls):
        server = websockets.serve(Server.userHandler, "localhost", 31666)
        logger.info("Server started.")
        
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
