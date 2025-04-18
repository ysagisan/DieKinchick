from aiogram import F, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from botSettings.createBot import dp
from rooms.createManager import manager
import keyboards.keyboards as kb


@dp.message(F.text == "❤️")
async def like(message: Message):
    pass

@dp.message(F.text == "👎")
async def dislike(message: Message):
    pass


@dp.message(F.text == "Уйти")
async def leave(message: Message):
    manager.deleteUser(message.from_user.id)
    await message.answer(f"пользователь {message.from_user.username} вышел из комнаты!", reply_markup=kb.startMenu)

def register_handlers(dp: Dispatcher):
    dp.message.register(like, F.text == "❤️")
    dp.message.register(dislike, F.text == "👎")
    dp.message.register(leave, F.text == "Уйти")
