from typing import List, Dict

class Room:
    def __init__(self, roomId: int, creatorId: int):
        self.roomId = roomId
        self.creatorId = creatorId
        self.roomMembers = [creatorId]
        self.match = list()

    def addMember(self, member):
        self.roomMembers.append(member)

