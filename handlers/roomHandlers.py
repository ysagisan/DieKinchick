from aiogram import F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import keyboards.keyboards as kb
from botSettings.createBot import dp, bot
from rooms.createManager import manager


class RoomStates(StatesGroup):
    waiting_for_room = State()
    in_room = State()


@dp.message(F.text == "Создать комнату")
async def createRoom(message: Message):
    roomId = manager.createRoom(message.from_user.id)
    await message.answer(f"вот id твоей комнаты: {roomId}, подожди друзей", reply_markup=kb.preStartMenu)


# @dp.callback_query_handler(F.text == "Создать комнату")
# async def user_id_inline_callback(callback_query: CallbackQuery):
#
#     await callback_query.answer(f"Ваш ID: {callback_query.from_user.id}", True)

@dp.message(F.text == "Подключиться к комнате")
async def connectToRoom(message: Message, state: FSMContext):
    # тут логика подключения
    await message.answer("Скажи пароль)))", reply_markup=kb.cancelMenu)
    await state.set_state(RoomStates.waiting_for_room)


@dp.message(RoomStates.waiting_for_room)
async def process_room_id(message: Message, state: FSMContext):
    room_id = int(message.text.strip())

    if manager.checkRoomId(room_id):
        manager.joinToRoom(room_id, message.from_user.id)
        # if roomManager.add_user_to_room(room_id, message.from_user.id):
        await message.answer(f"Вы успешно подключились к комнате {room_id}!", reply_markup=kb.preStartMenu)
        await state.set_state(RoomStates.in_room)
        creator_id = manager.getCreatorId(room_id)

        await bot.send_message(creator_id,
                               f"Пользователь @{message.from_user.username} подключился к вашей комнате!")
    else:
        await message.answer("Комната с таким ID не найдена. Попробуйте еще раз или создайте новую комнату.",
                             reply_markup=kb.preStartMenu)
        await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(createRoom, F.text == "Создать комнату")
    dp.message.register(connectToRoom, F.text == "Подключиться к комнате")
    dp.message.register(process_room_id, RoomStates.waiting_for_room)