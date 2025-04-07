from aiogram import F, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from createBot import dp

import keyboards.keyboards as kb


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)


@dp.message(F.text == "Поехали! 🚜")
async def roomMenu(message: Message):
    await message.answer("выбери свой путь........", reply_markup=kb.roomMenu)

@dp.message(F.text == "Создать комнату")
async def preStartMenu(message: Message):
    #создание комнаты
    await message.answer("подожди друзей", reply_markup=kb.preStartMenu)

@dp.message(F.text == "Подключиться к комнате")
async def preStartMenu(message: Message):
    #тут логика подключения
    await message.answer("Скажи пароль)))", reply_markup=kb.cancelMenu)

@dp.message(F.text == "Начать подбор фильма")
async def likeDislikeMenu(message: Message):
    data = func()
    await message.answer(data)
    # await message.answer("подожди друзей", reply_markup=kb.likeDislikeMenu)

@dp.message(F.text == "❤️")
async def likeDislikeMenu(message: Message):
    pass


@dp.message(F.text == "👎")
async def likeDislikeMenu(message: Message):
    pass

@dp.message(F.text == "Отмена")
async def likeDislikeMenu(message: Message):
    await message.answer("привет бродяга 😎", reply_markup=kb.startMenu)
