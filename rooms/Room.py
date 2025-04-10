from typing import List, Dict

class Room:
    def __init__(self, roomId: int, creatorId: int):
        self.roomId = roomId
        self.creatorId = creatorId
        self.roomMembers: List[int] = [creatorId]

    def addMember(self, member):
        self.roomMembers.append(member)