from aiogram import F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from botSettings.createBot import dp
from aiogram.fsm.state import StatesGroup, State

import keyboards.keyboards as kb

'''from api_gateway.film_service import get_film_data, get_kinopoisk_id_by_title # файлы в ветке find_film_service

class FilmSearchState(StatesGroup):   # для понимания контекста бота, типа он ждет сообщения с названием фильма
    waiting_for_title = State()

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
            poster_url = film_data.get("poster_url")

            # Формируем сообщение с постером и информацией о фильме
            if poster_url:
                await message.answer_photo(poster_url, caption=f"Название: {name}\nГод: {year}\nЖанр: {genre}\nРейтинг: {rating}\nОписание: {description}")
            else:
                await message.answer(f"Постер для фильма {name} не найден.\n\nОписание:\n{description}")
        else:
            await message.answer("Фильм не найден.")
    else:
        await message.answer("Фильм не найден в базе.")'''


@dp.message(F.text == "Начать подбор фильма")
async def likeDislikeMenu(message: Message):
    await message.answer("подожди друзей", reply_markup=kb.likeDislikeMenu)

def register_handlers(dp: Dispatcher):
    dp.message.register(likeDislikeMenu, F.text == "Начать подбор фильма")
