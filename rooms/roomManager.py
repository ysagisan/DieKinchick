from typing import Dict
from Room import Room
from random import choice

class RoomManager:
    def __init__(self):
        self.idsRange = list(range(100000, 1000001))
        self.nonAvalibleIds = set()
        self.activeRooms = dict()

    def createUniqueId(self):
        newId = choice(self.idsRange)
        while newId in self.nonAvalibleIds:
            newId = choice(self.idsRange)
        self.nonAvalibleIds.add(newId)
        return newId

    def createRoom(self, creatorId: int) -> Room:
        roomId = self.createUniqueId()
        room = Room(roomId, creatorId)
        self.activeRooms[roomId] = room
        return room

    def deleteRoom(self):
        pass