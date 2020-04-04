import asyncio
import ssl

import websockets

from src.util.Logger import logger
from src.room.RoomList import RoomList
from src.player.Player import Player


class Server:
    __ID = 0
    
    @classmethod
    async def userHandler(cls, websocket: websockets.WebSocketClientProtocol, _):  # _ is path.
        player = Player(cls.__ID, websocket)
        cls.__ID += 1
        logger.info(player.getAddress() + " has connected.")
        roomID = RoomList.addPlayer(player)
        await player.joinTheRoom()
        RoomList.removeRoom(roomID)
        logger.info("The game in room #{} has been done.".format(roomID))
    
    @classmethod
    def run(cls, path):
        path = "/".join(path.split("/")[:-1]) + "/certificates/"
        
        sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        cert = path + "cert.pem"
        key = path + "key.pem"
        sslContext.load_cert_chain(cert, key)

        server = websockets.serve(Server.userHandler, "localhost", 31666, ssl=sslContext)
        logger.info("Server started.")
        
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
