import asyncio
import logging
import pathlib
import ssl

import websockets

from src.room.RoomList import RoomList
from src.player.Player import Player


class Server:
    __ID = 0
    
    @classmethod
    async def userHandler(cls, websocket: websockets.WebSocketClientProtocol, _):  # _ is path.
        player = Player(cls.__ID, websocket)
        cls.__ID += 1
        logging.info("%s has connected.", player.getAddress())
        roomID = RoomList.addPlayer(player)
        await player.joinTheRoom()
        RoomList.removeRoom(roomID)
    
    @staticmethod
    def setupLogger():
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
        
        logging.getLogger('asyncio').setLevel(logging.WARNING)
        logging.getLogger('asyncio.coroutines').setLevel(logging.WARNING)
        logging.getLogger('websockets.server').setLevel(logging.WARNING)
        logging.getLogger('websockets.protocol').setLevel(logging.WARNING)
    
    @classmethod
    def run(cls, path):
        path = "/".join(path.split("/")[:-1]) + "/certificates/"
        
        Server.setupLogger()
        
        sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        cert = path + "cert.pem"
        key = path + "key.pem"
        sslContext.load_cert_chain(cert, key)

        server = websockets.serve(Server.userHandler, "localhost", 31666, ssl=sslContext)
        logging.info("Server started.")
        
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
