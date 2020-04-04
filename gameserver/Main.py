import asyncio
import ssl
import pathlib
import logging
import websockets


games = list()
Id = 0


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
                await player.sendMessage("Game!")
    
    async def __keepConnected(self):
        while not self.__finished:
            await asyncio.sleep(2)
    
    def isFull(self) -> bool:
        return len(self.__players) == self.__size
    
    def setID(self, ID: int):
        if self.__ID is None:
            self.__ID = ID


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
    
    async def joinTheRoom(self):
        while not self.__room.isFull():
            await asyncio.sleep(1)
            await self.__websocket.send("Ping!")
        await self.__room.start()
    
    def setRoom(self, room: Room):
        if self.__room is None:
            self.__room = room


class RoomList:
    __rooms = dict()
    
    @classmethod
    def addPlayer(cls, player: Player) -> bool:
        """
        Returns True if found a game and False if queued.
        """
        for room in cls.__rooms.values():
            if room.tryToAddPlayer(player):
                cls.__addRoom(2)
                player.setRoom(room)
                return True

        room = cls.__addRoom(2)
        if room.tryToAddPlayer(player):
            player.setRoom(room)
            return False

        logging.error("Unable to add a user to the room!")
        raise ValueError("Unable to add a user to the room!")
            
    
    @classmethod
    def __addRoom(cls, size: int) -> Room:
        for i in range(50):  # Room limit of 50.
            if i not in cls.__rooms.keys():
                cls.__rooms[i] = Room(size)
                return cls.__rooms[i]
    
        logging.warning("Reached room limit!")
        raise OverflowError("Reached room limit!")
    
    @classmethod
    def removeRoom(cls, roomID: int):
        cls.__rooms[roomID] = None


async def userHandler(websocket: websockets.WebSocketClientProtocol, _):  # _ is path.
    global Id
    player = Player(Id, websocket)
    Id += 1
    logging.info("%s has connected.", player.getAddress())
    RoomList.addPlayer(player)
    await player.joinTheRoom()


sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
cert = pathlib.Path(__file__).with_name("cert.pem")
key = pathlib.Path(__file__).with_name("key.pem")
sslContext.load_cert_chain(cert, key)

server = websockets.serve(userHandler, "localhost", 31666, ssl=sslContext)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
