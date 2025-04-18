from aiogram import F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api_gateway.film_service import get_recommended_film_with_genre, get_kinopoisk_id_by_title, get_film_data
from api_gateway.film_service import get_recommended_films
from botSettings.createBot import dp
from aiogram.fsm.state import StatesGroup, State
import keyboards.keyboards as kb
from handlers.mainHandlers import cancelForSearch
from rooms.createManager import manager

class FilmSearchState(StatesGroup):   # для понимания контекста бота, типа он ждет сообщения с названием фильма
    waiting_for_title = State()

class FilmRecommendationState(StatesGroup): # для состояния, когда пользователь оценивает фильмы
    recommendation = State()

class FilmGenreChoiceState(StatesGroup): # для состояния выбора жанра
    choosing_genre = State()

@dp.message(F.text == "Найти фильм")       # для поиска фильма
async def ask_for_title(message: Message, state: FSMContext):
    await message.answer("Введи название фильма", reply_markup=kb.searchMenu)
    await state.set_state(FilmSearchState.waiting_for_title)

@dp.message(FilmSearchState.waiting_for_title)  # здесь и происходит поиск фильма
async def film_info(message: Message, state: FSMContext):
    title = message.text.strip()

    kinopoisk_id = get_kinopoisk_id_by_title(title) # сначала получаем id фильма через название, которое ввел пользователь
    if kinopoisk_id:
        film_data = get_film_data(kinopoisk_id) # потом по этому id находим сам фильм

        if film_data:
            name = film_data.get("name")
            year = film_data.get("year")
            genre = film_data.get("genre")
            rating = film_data.get("rating")
            description = film_data.get("description")
            webUrl = film_data.get("webUrl")
            poster_url = film_data.get("poster_url")

            # Формируем сообщение с постером и информацией о фильме
            if poster_url:
                await message.answer_photo(poster_url, caption=f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}\nОписание: {description}\n\nПодробнее: {webUrl}",
                    reply_markup=kb.searchMenu
                )
            else:
                await message.answer(f"Постер для фильма {name} не найден.\n\nОписание:\n{description}\n\nПодробнее: {webUrl}")
        else:
            await message.answer("Фильм не найден.")
    else:
        await message.answer("Фильм не найден в базе.")

async def send_film(message: Message, state: FSMContext):
    user_data = await state.get_data()
    films = user_data.get("films", [])
    index = user_data.get("index", 0)

    # Проверяем, есть ли фильмы для отправки
    if index < len(films):
        film = films[index]
        name = film["name"]
        year = film["year"]
        genre = film["genre"]
        rating = film["rating"]
        webUrl = film["webUrl"]
        description = film["description"]
        poster_url = film["poster_url"]

        # Отправляем постер и информацию о фильме
        if poster_url:
            await message.answer_photo(
                poster_url,
                caption=f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}\nОписание: {description}\n\nПодробнее: {webUrl}",
                reply_markup=kb.likeDislikeMenu
            )
        else:
            await message.answer(
                f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}\nОписание: {description}\n\nПодробнее: {webUrl}",
                reply_markup=kb.likeDislikeMenu
            )

        await state.update_data(index=index + 1)
    else:
        await message.answer("Вы просмотрели все фильмы!")

@dp.message(F.text == "Начать без выбора жанра")
async def start_recommendation(message: Message, state: FSMContext):
    films = get_recommended_films(limit=10)

    if not films:
        await message.answer("Не удалось загрузить фильмы.")
        return

    await state.update_data(films=films, index=0)
    await state.set_state(FilmRecommendationState.recommendation)
    await send_film(message, state)

@dp.message(FilmRecommendationState.recommendation)
async def rate_film(message: Message, state: FSMContext):
    user_data = await state.get_data()
    films = user_data.get("films", [])
    index = user_data.get("index", 0)

    if index <= 0:
        return

    film = films[index - 1]  # Получаем фильм который был показан
    film_name = film["name"]

    if message.text == "❤️":
        await message.answer(f"Вы поставили лайк фильму: {film_name}")
    elif message.text == "👎":
        await message.answer(f"Вы поставили дизлайк фильму: {film_name}")
    else:
        return

    await send_film(message, state)

@dp.message(F.text == "Выбрать жанр")
async def choose_genre(message: Message, state: FSMContext):
    await message.answer("Выбери жанр фильма:", reply_markup=kb.genreMenu)
    await state.set_state(FilmGenreChoiceState.choosing_genre)

@dp.message(FilmGenreChoiceState.choosing_genre)
async def start_recommendation_with_genre(message: Message, state: FSMContext):
    genre = message.text.strip()
    await message.answer(f"Подбираю фильмы в жанре: {genre}...")

    films = get_recommended_film_with_genre(limit=10, genre=genre)

    if not films:
        await message.answer("Не удалось загрузить фильмы.")
        return

    await state.update_data(films=films, index=0)
    await state.set_state(FilmRecommendationState.recommendation)
    await send_film(message, state)

@dp.message(F.text == "Уйти")
async def leave(message: Message, state: FSMContext):
    manager.deleteUser(message.from_user.id)
    await message.answer(f"пользователь {message.from_user.username} вышел из комнаты!", reply_markup=kb.startMenu)
    await state.clear()

def register_handlers(dp: Dispatcher):
    dp.message.register(choose_genre, F.text == "Выбрать жанр")
    dp.message.register(leave, F.text == "Уйти")
    dp.message.register(cancelForSearch, F.text == "Отмена")
    dp.message.register(start_recommendation_with_genre, FilmGenreChoiceState.choosing_genre)
    dp.message.register(start_recommendation, F.text == "Начать без выбора жанра")
    dp.message.register(ask_for_title, F.text == "Найти фильм")
    dp.message.register(film_info, FilmSearchState.waiting_for_title)
    dp.message.register(rate_film, FilmRecommendationState.recommendation)