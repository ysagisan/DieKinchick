from typing import List, Dict

class Room:
    def __init__(self, roomId: int, creatorId: int):
        self.roomId = roomId
        self.creatorId = creatorId
        self.roomMembers = []  # удалил creatorId, потому что здесь список объектов, а не список айдишников
        self.match = list()
        self.films = [] # список фильмов для комнаты
        self.userIndex = dict() # словарь с индексами текущего фильма для каждого пользователя
        self.matched_films = []  # список совпавших фильмов
        self.finished_users = set()  # user_id пользователей, закончивших просмотр

    def addMember(self, member):
        self.roomMembers.append(member)
        self.userIndex[member.userId] = 0

    def deleteMember(self, user):
        self.roomMembers.remove(user)

    def getCreatorId(self):
        return self.creatorId

    def getCurrentFilmForUser(self, userId):
        ind = self.userIndex.get(userId, 0)
        if ind < len(self.films):
            return self.films[ind]
        return None

    def nextFilmForUser(self, userId):
        self.userIndex[userId] = self.userIndex.get(userId, 0) + 1

    def setFilms(self, films):
        self.films = films
        for user in self.roomMembers:
            self.userIndex[user] = 0

    def getRoomId(self):
        return self.roomId