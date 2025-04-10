from aiogram import F, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from botSettings.createBot import dp

import keyboards.keyboards as kb


class FilmSearchState(StatesGroup):   # для понимания контекста бота, типа он ждет сообщения с названием фильма
    waiting_for_title = State()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)


@dp.message(F.text == "Поехали! 🚜")
async def roomMenu(message: Message):
    await message.answer("выбери свой путь........", reply_markup=kb.roomMenu)


@dp.message(F.text == "Отмена")
async def cancel(message: Message, state: FSMContext):
    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)
    await state.clear()  # добавил для восттановления контекста бота, чтобы не из любого меню можно было запустить film_info


def register_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(roomMenu, F.text == "Поехали! 🚜")
    dp.message.register(cancel, F.text == "Отмена")


