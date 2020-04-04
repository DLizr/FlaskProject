import logging

from src.room.Room import Room
from src.player.Player import Player


class RoomList:
    __rooms = dict()
    
    @classmethod
    def addPlayer(cls, player: Player) -> int:
        """
        Returns room ID.
        """
        for room in cls.__rooms.values():
            if room.tryToAddPlayer(player):
                player.setRoom(room)
                return room.getID()

        room = cls.__addRoom(2)
        if room.tryToAddPlayer(player):
            player.setRoom(room)
            return room.getID()

        logging.error("Unable to add a user to the room!")
        raise ValueError("Unable to add a user to the room!")
            
    
    @classmethod
    def __addRoom(cls, size: int) -> Room:
        for i in range(50):  # Room limit of 50.
            if i not in cls.__rooms.keys():
                cls.__rooms[i] = Room(size)
                cls.__rooms[i].setID(i)
                return cls.__rooms[i]
    
        logging.warning("Reached room limit!")
        raise OverflowError("Reached room limit!")
    
    @classmethod
    def removeRoom(cls, roomID: int):
        cls.__rooms.pop(roomID)
