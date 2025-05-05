from aiogram import F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import requests
import keyboards.keyboards as kb
from botSettings.createBot import dp, bot
from rooms.createManager import manager
from handlers.mainHandlers import cancel, cancelFromEnterPassword

class RoomStates(StatesGroup):
    waiting_for_room = State()
    in_room = State()


@dp.message(F.text == "🆕 Создать комнату")
async def createRoom(message: Message):
    roomId = manager.createRoom(message.from_user.id)
    await message.answer(f"Вот id твоей комнаты: {roomId}\nПодожди друзей", reply_markup=kb.preStartMenu)
    manager.joinToRoom(roomId, message.from_user.id)   # добавил, потому что когда пользователь создавал комнату у него не обновлялся id комнаты, то есть он был -1


@dp.message(F.text == "👥 Присоединиться")
async def connectToRoom(message: Message, state: FSMContext):
    # тут логика подключения
    await message.answer("Скажи пароль)))", reply_markup=kb.enterPasswordMenu)
    await state.set_state(RoomStates.waiting_for_room)


@dp.message(RoomStates.waiting_for_room)
async def process_room_id(message: Message, state: FSMContext):
    room_id = int(message.text.strip())
    if manager.checkRoomId(room_id) == 1:
        manager.joinToRoom(room_id, message.from_user.id)

        updated_users = [user.getUserId() for user in manager.getRoomById(room_id).roomMembers]
        if len(updated_users) > 1:
            try:
                response = requests.post("http://match_api:4450/push", params={
                    "status": "new room",  # Переиспользуем этот статус
                    "room": room_id,
                    "users": updated_users
                })
            except Exception as e:
                print(f"Ошибка при обновлении пользователей комнаты: {e}")

        await message.answer(f"Вы успешно подключились к комнате {room_id}!\nОжидайте", reply_markup=kb.menuForConnectedUsers)
        await state.set_state(RoomStates.in_room)
        creator_id = manager.getCreatorId(room_id)

        await bot.send_message(creator_id,
                               f"Пользователь @{message.from_user.username} подключился к вашей комнате!")
    else:
        await message.answer("Комната с таким ID не найдена. Попробуйте еще раз или создайте новую комнату.",
                             reply_markup=kb.roomMenu)
        await state.clear()

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
    dp.message.register(createRoom, F.text == "🆕 Создать комнату")
    dp.message.register(connectToRoom, F.text == "👥 Присоединиться")
    dp.message.register(leave, F.text == "🚪 Уйти")
    dp.message.register(cancelFromEnterPassword, F.text == "❌ Отмена")
    dp.message.register(process_room_id, RoomStates.waiting_for_room)