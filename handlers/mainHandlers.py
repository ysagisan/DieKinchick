from aiogram import F, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from botSettings.createBot import dp

import keyboards.keyboards as kb
from rooms.createManager import manager


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)


@dp.message(F.text == "Поехали! 🚜")
async def roomMenu(message: Message):
    manager.addNewUser(message.from_user.id)
    await message.answer("выбери свой путь........", reply_markup=kb.roomMenu)


@dp.message(F.text == "🔄 Отмена")
async def cancel(message: Message, state: FSMContext):
    curUser = manager.getUserById(message.from_user.id)
    room = manager.getRoomById(curUser.getRoomNumber())

    manager.deleteUser(message.from_user.id)
    manager.deleteUserFromRoom(curUser, room)

    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)
    await state.clear()  # добавил для восттановления контекста бота, чтобы не из любого меню можно было запустить film_info


@dp.message(F.text == "🚫 Закрыть поиск")
async def cancelForSearch(message: Message, state: FSMContext):
    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)
    await state.clear()  # добавил для восттановления контекста бота, чтобы не из любого меню можно было запустить film_info


@dp.message(F.text == "❌ Отмена")
async def cancelFromEnterPassword(message: Message, state: FSMContext):
    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)
    await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(roomMenu, F.text == "Поехали! 🚜")
    dp.message.register(cancel, F.text == "🔄 Отмена")
