import unittest
from rooms.User import User
from rooms.Manager import Manager


class TestRoom(unittest.TestCase):
    def setUp(self):
        print("test set up")
        self.manager = Manager()
        self.creator_id = 1
        self.user1 = User(self.creator_id)
        self.manager.addNewUser(self.creator_id)
        self.room_id = self.manager.createRoom(self.creator_id)
        self.room = self.manager.getRoomById(self.room_id)
        self.user2 = User(2)
        self.manager.addNewUser(self.user2.userId)
        self.user3 = User(3)
        self.manager.addNewUser(self.user3.userId)
        self.films = ["Film1", "Film2", "Film3"]

    def test_init(self):
        print("test init")
        self.assertEqual(self.room.roomId, self.room_id)
        self.assertEqual(self.room.creatorId, self.creator_id)
        self.assertEqual(self.room.roomMembers, [])
        self.assertEqual(self.room.match, [])
        self.assertEqual(self.room.films, [])
        self.assertEqual(self.room.userIndex, {})

    def test_add_member(self):
        print("test add member")
        self.room.addMember(self.user2)
        self.assertIn(self.user2, self.room.roomMembers)
        self.assertEqual(self.room.userIndex[self.user2.userId], 0)

    def test_delete_member(self):
        print("test delete member")
        self.room.addMember(self.user2)
        self.room.deleteMember(self.user2)
        self.assertNotIn(self.user2, self.room.roomMembers)
        self.assertIn(self.user2.userId, self.room.userIndex)  # userIndex не очищается

    def test_get_creator_id(self):
        print("test get creator id")
        self.assertEqual(self.room.getCreatorId(), self.creator_id)

    def test_get_current_film_for_user_no_films(self):
        print("test get current film for user no films")
        self.room.addMember(self.user2)
        self.assertIsNone(self.room.getCurrentFilmForUser(self.user2.userId))

    def test_get_current_film_for_user(self):
        print("test get current film for user")
        self.room.addMember(self.user2)
        self.room.setFilms(self.films)
        self.assertEqual(self.room.getCurrentFilmForUser(self.user2.userId), "Film1")

    def test_get_current_film_for_user_after_next(self):
        print("test get current film for user after next")
        self.room.addMember(self.user2)
        self.room.setFilms(self.films)
        self.room.nextFilmForUser(self.user2.userId)
        self.assertEqual(self.room.getCurrentFilmForUser(self.user2.userId), "Film2")

    def test_get_current_film_for_user_beyond_films(self):
        print("test get current film for user beyond films")
        self.room.addMember(self.user2)
        self.room.setFilms(self.films)
        self.room.nextFilmForUser(self.user2.userId)
        self.room.nextFilmForUser(self.user2.userId)
        self.room.nextFilmForUser(self.user2.userId)
        self.assertIsNone(self.room.getCurrentFilmForUser(self.user2.userId))

    def test_next_film_for_user(self):
        print("test next film for user")
        self.room.addMember(self.user2)
        self.room.setFilms(self.films)
        self.room.nextFilmForUser(self.user2.userId)
        self.assertEqual(self.room.userIndex[self.user2.userId], 1)

    def test_set_films(self):
        print("test set films")
        self.room.addMember(self.user2)
        self.room.addMember(self.user3)
        self.room.setFilms(self.films)
        self.assertEqual(self.room.films, self.films)
        self.assertEqual(self.room.userIndex[self.user2.userId], 0)
        self.assertEqual(self.room.userIndex[self.user3.userId], 0)

    def test_get_room_id(self):
        print("test get room id")
        self.assertEqual(self.room.getRoomId(), self.room_id)


if __name__ == '__main__':
    unittest.main()
