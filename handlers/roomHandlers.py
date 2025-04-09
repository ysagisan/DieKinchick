from aiogram import  F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import keyboards.keyboards as kb
from botSettings.createBot import dp


class RoomStates(StatesGroup):
    waiting_for_room = State()
    in_room = State()


# @dp.message(F.text == "Создать комнату")
# async def preStartMenu(message: Message):
#     #создание комнаты
#     await message.answer("подожди друзей", reply_markup=kb.preStartMenu)

@dp.callback_query_handler(F.text == "Создать комнату")
async def user_id_inline_callback(callback_query: CallbackQuery):

    await callback_query.answer(f"Ваш ID: {callback_query.from_user.id}", True)

@dp.message(F.text == "Подключиться к комнате")
async def preStartMenu(message: Message):
    #тут логика подключения
    await message.answer("Скажи пароль)))", reply_markup=kb.cancelMenu)