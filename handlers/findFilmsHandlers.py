from aiogram import F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message

from api_gateway.film_service import get_recommended_film_with_genre, get_kinopoisk_id_by_title, get_film_data
from api_gateway.film_service import get_recommended_films
from botSettings.createBot import dp, bot
from aiogram.fsm.state import StatesGroup, State
import keyboards.keyboards as kb
from handlers.mainHandlers import cancelForSearch, cancel
from rooms.createManager import manager


class FilmSearchState(StatesGroup):  # для понимания контекста бота, типа он ждет сообщения с названием фильма
    waiting_for_title = State()


class FilmRecommendationState(StatesGroup):  # для состояния, когда пользователь оценивает фильмы
    recommendation = State()


class FilmGenreChoiceState(StatesGroup):  # для состояния выбора жанра
    choosing_genre = State()


@dp.message(F.text == "🔍 Найти фильм")  # для поиска фильма
async def ask_for_title(message: Message, state: FSMContext):
    await message.answer("Введи название фильма", reply_markup=kb.searchMenu)
    await state.set_state(FilmSearchState.waiting_for_title)


@dp.message(FilmSearchState.waiting_for_title)  # здесь и происходит поиск фильма
async def film_info(message: Message, state: FSMContext):
    title = message.text.strip()

    kinopoisk_id = get_kinopoisk_id_by_title(
        title)  # сначала получаем id фильма через название, которое ввел пользователь
    if kinopoisk_id:
        film_data = get_film_data(kinopoisk_id)  # потом по этому id находим сам фильм

        if film_data:
            name = film_data.get("name")
            year = film_data.get("year")
            genre = film_data.get("genre")
            rating = film_data.get("rating")
            description = film_data.get("description")
            webUrl = film_data.get("webUrl")
            poster_url = film_data.get("poster_url")

            # Формируем сообщение с постером и информацией о фильме
            text = f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}\nОписание: {description}\n\nПодробнее: {webUrl}"
            if poster_url:
                if len(text) > 1024:
                    await message.answer_photo(poster_url,
                                               f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}")
                    await message.answer(f"Описание: {description}\n\nПодробнее: {webUrl}", reply_markup=kb.searchMenu)
                else:
                    await message.answer_photo(poster_url, caption=text, reply_markup=kb.searchMenu)
            else:
                await message.answer(
                    f"Постер для фильма {name} не найден.\n\nОписание:\n{description}\n\nПодробнее: {webUrl}")
        else:
            await message.answer("Фильм не найден.")
    else:
        await message.answer("Фильм не найден в базе.")


async def send_room_film(message: Message, state: FSMContext, room,
                         userId):  # здесь отправляем фильм в конкретный чат конкретному пользователю

    film = room.getCurrentFilmForUser(userId)

    if not film:
        await message.answer("Вы просмотрели все фильмы!")
        return

    poster_url = film["poster_url"]
    name = film["name"]
    year = film["year"]
    genre = film["genre"]
    rating = film["rating"]
    webUrl = film["webUrl"]
    description = film["description"]

    text = f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}\nОписание: {description}\n\nПодробнее: {webUrl}"

    if poster_url:
        if len(text) > 1024:
            await bot.send_photo(userId, poster_url, f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}")
            await bot.send_message(userId, f"Описание: {description}\n\nПодробнее: {webUrl}",
                                   reply_markup=kb.likeDislikeMenu)
        else:
            await bot.send_photo(userId, poster_url, caption=text, reply_markup=kb.likeDislikeMenu)
    else:
        await bot.send_message(userId, text, reply_markup=kb.likeDislikeMenu)

    room.nextFilmForUser(userId)


@dp.message(
    F.text == "🎲 Случайный подбор")  # здесь задается список фильмов и для каждого пользователя устанавливается контекст рекомендации
async def start_recommendation(message: Message, state: FSMContext):
    user = manager.getUserById(message.from_user.id)
    room = manager.getRoomById(user.getRoomNumber())

    if not room.films:
        room.setFilms(get_recommended_films(limit=10))

    for curUser in room.roomMembers:
        userId = curUser.getUserId()

        # создаем отдельный контекст для каждого участника
        individual_state = FSMContext(
            storage=state.storage,
            key=StorageKey(
                bot_id=bot.id,
                chat_id=userId,
                user_id=userId
            )
        )
        await individual_state.set_state(FilmRecommendationState.recommendation)
        await send_room_film(message, individual_state, room, userId)


@dp.message(FilmRecommendationState.recommendation)  # здесь пользователи оценивают фильм и отправляется следующий
async def rate_film(message: Message, state: FSMContext):
    user = manager.getUserById(message.from_user.id)
    room = manager.getRoomById(user.getRoomNumber())

    lastIndex = room.userIndex.get(user.userId, 1) - 1
    if lastIndex < 0 or lastIndex >= len(room.films):
        return

    film = room.films[lastIndex]
    film_name = film["name"]

    if message.text == "❤️":
        await message.answer(f"Вы поставили лайк фильму: {film_name}")
    elif message.text == "👎":
        await message.answer(f"Вы поставили дизлайк фильму: {film_name}")
    else:
        return

    await send_room_film(message, state, room, message.from_user.id)


@dp.message(F.text == "🎭 Выбрать жанр")
async def choose_genre(message: Message, state: FSMContext):
    await message.answer("Выбери жанр фильма:", reply_markup=kb.genreMenu)
    await state.set_state(FilmGenreChoiceState.choosing_genre)


@dp.message(FilmGenreChoiceState.choosing_genre)
async def start_recommendation_with_genre(message: Message, state: FSMContext):
    genre = message.text.strip()
    await message.answer(f"Подбираю фильмы в жанре: {genre}...")

    films = get_recommended_film_with_genre(limit=10, genre=genre)

    user = manager.getUserById(message.from_user.id)
    room = manager.getRoomById(user.getRoomNumber())

    if not room.films:
        room.setFilms(films)

    for curUser in room.roomMembers:
        userId = curUser.getUserId()

        # создаем отдельный контекст для каждого участника
        individual_state = FSMContext(
            storage=state.storage,
            key=StorageKey(
                bot_id=bot.id,
                chat_id=userId,
                user_id=userId
            )
        )
        await individual_state.set_state(FilmRecommendationState.recommendation)
        await send_room_film(message, individual_state, room, userId)


@dp.message(F.text == "🚪 Уйти")
async def leave(message: Message, state: FSMContext):
    curUser = manager.getUserById(message.from_user.id)
    room = manager.getRoomById(curUser.getRoomNumber())
    username = message.from_user.username

    manager.deleteUser(message.from_user.id)
    manager.deleteUserFromRoom(curUser, room)

    for user in room.roomMembers:
        userId = user.getUserId()
        await bot.send_message(userId, f"Пользователь @{username} вышел из комнаты!")

    await message.answer(f"Вы покинули комнату {room.getRoomId()}", reply_markup=kb.startMenu)
    await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(choose_genre, F.text == "🎭 Выбрать жанр")
    dp.message.register(leave, F.text == "🚪 Уйти")
    dp.message.register(cancel, F.text == "🔄 Отмена")
    dp.message.register(cancelForSearch, F.text == "🚫 Закрыть поиск")
    dp.message.register(start_recommendation_with_genre, FilmGenreChoiceState.choosing_genre)
    dp.message.register(start_recommendation, F.text == "🎲 Случайный подбор")
    dp.message.register(ask_for_title, F.text == "🔍 Найти фильм")
    dp.message.register(film_info, FilmSearchState.waiting_for_title)
    dp.message.register(rate_film, FilmRecommendationState.recommendation)
