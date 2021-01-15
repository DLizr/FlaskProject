import asyncio

import websockets

from src.util.Logger import logger
from src.room.RoomList import RoomList
from src.player.Player import Player

from src.website import HttpPipe


class Server:
    __ID = 0
    __cooldown = 0
    
    @classmethod
    async def userHandler(cls, websocket: websockets.WebSocketClientProtocol, _):  # _ is path.
        player = Player(websocket)
        if (not await cls.__verifyPlayer(player)):
            await player.sendMessageSafe("BAD_CODE")
            logger.warning(player.getAddress() + " has tried to connect but didn't pass the verification!")
            return
        
        cls.__cooldown += 4
        await asyncio.sleep(cls.__cooldown)  # Players can join once per 4 seconds.
        cls.__cooldown -= 4
        
        cls.__ID += 1
        logger.info(player.getAddress() + " has connected.")
        
        room = RoomList.addPlayer(player)
        await room.connectPlayer(player)
        
        RoomList.removeRoom(room.getID())
        await player.disconnect()
        logger.info("The game in room #{} is over.".format(room.getID()))
    
    @classmethod
    def run(cls):
        try:
            server = websockets.serve(Server.userHandler, "localhost", 31666, max_queue=2000000)
            logger.info("Server started.")
            
            HttpPipe.run()
            
            asyncio.get_event_loop().run_until_complete(server)
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            logger.info("Stopped the socket server.")
            logger.info("Stopping HTML server...")
            HttpPipe.stop()
            logger.info("Stopped HTML server.")
    
    @staticmethod
    async def __verifyPlayer(player: Player):
        for _ in range(5):
            code = player.getMessageIfReceived()
            if code:
                break
            await asyncio.sleep(1)
        else:
            return False
        
        try:
            playerId = HttpPipe.players.pop(code)
        except KeyError:
            return False
        
        player.setId(playerId)
        return True
