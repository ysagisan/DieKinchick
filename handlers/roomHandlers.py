from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import keyboards.keyboards as kb
from botSettings.createBot import dp


class RoomStates(StatesGroup):
    waiting_for_room = State()
    in_room = State()


@dp.message(F.text == "Создать комнату")
async def createRoom(message: Message):
    #создание комнаты
    await message.answer("подожди друзей", reply_markup=kb.preStartMenu)

# @dp.callback_query_handler(F.text == "Создать комнату")
# async def user_id_inline_callback(callback_query: CallbackQuery):
#
#     await callback_query.answer(f"Ваш ID: {callback_query.from_user.id}", True)

@dp.message(F.text == "Подключиться к комнате")
async def connectToRoom(message: Message):
    #тут логика подключения
    await message.answer("Скажи пароль)))", reply_markup=kb.cancelMenu)
    

def register_handlers(dp: Dispatcher):
    dp.message.register(createRoom, F.text == "Создать комнату")
    dp.message.register(connectToRoom, F.text == "Подключиться к комнате")