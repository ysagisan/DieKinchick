class User:
    def __init__(self, userId):
        self.userId = userId
        self.roomNumber = -1

    def assignToRoom(self, roomNumber):
        self.roomNumber = roomNumber

    def leaveRoom(self):
        self.roomNumber = -1

    def getRoomNumber(self):
        return self.roomNumber


    def getUserId(self):
        return self.userId
