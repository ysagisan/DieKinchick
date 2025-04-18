from rooms.User import User
from rooms.Room import Room
from random import choice


# from rooms.createManagers import userManager

class Manager:
    def __init__(self):
        self.idsRange = list(range(100000, 1000001))
        self.nonAvalibleIds = set()
        self.activeRooms = list() #Room
        self.userList = list()

    def getUserById(self, userId):
        for user in self.userList:
            if user.userId == userId:
                return user
        return None

    def addNewUser(self, userId):
        newUser = User(userId)
        print(f"new user added: {userId}")
        self.userList.append(newUser)

    def deleteUser(self, userId):
        print(f"user leave us: {userId}")
        removedUser = self.getUserById(userId)
        if removedUser:
            self.userList.remove(removedUser)

    def getLastUser(self):
        return self.userList[-1]

    def createUniqueId(self):
        newId = choice(self.idsRange)
        while newId in self.nonAvalibleIds:
            newId = choice(self.idsRange)
        self.nonAvalibleIds.add(newId)
        return newId

    def createRoom(self, creatorId: int) -> int:
        roomId = self.createUniqueId()
        room = Room(roomId, creatorId)
        self.activeRooms.append(room)
        return roomId

    def getRoomById(self, roomId):
        for room in self.activeRooms:
            print(room.roomId)
            if room.roomId == roomId:
                print(f"from getRoomById {room} !!!!!!!!!!!!!!!!!!!!")
                return room
        return None

    def deleteRoom(self, room: Room):
        self.nonAvalibleIds.remove(room.roomId)
        self.activeRooms.remove(room)


    def joinToRoom(self, roomId, userId):
        newUser = self.getUserById(userId)
        if newUser:
            print(f"user {newUser} joined to room")
            self.getRoomById(roomId).addMember(newUser)
            print(self.activeRooms)
            newUser.assignToRoom(roomId)
        return 0

    def checkRoomIsNotEmpty(self, room: Room):
        return len(room.roomMembers)

    def leaveRoom(self, userId):
        leaveUser = self.getUserById(userId)
        if leaveUser:
            print(f"user {leaveUser} leaved to room")
            roomId = leaveUser.getRoomNumber()
            room = self.getRoomById(roomId)
            room.deleteMember(leaveUser)
            leaveUser.leaveRoom()
            if not self.checkRoomIsNotEmpty(room):
                self.deleteRoom(roomId)

    def checkRoomId(self, roomId):
        if roomId in self.activeRooms:
            return 1
        return -1

    def getCreatorId(self, roomId):
        return self.getRoomById(roomId).getCreatorId()