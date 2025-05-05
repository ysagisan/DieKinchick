from aiogram import F, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
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

@dp.message(Command("info"))
async def help_command(message: types.Message):
    text = ("Этот бот создан для легкого выбора фильма для просмотра со своими друзьями 👀\n\n"
            "1️⃣ Один из Вас может создать комнату, нажав на кнопку «🆕 Создать комнату»\n\n"
            "2️⃣ Остальные могут присоединиться к вашей комнате нажав на кнопку «👥 Присоединиться» и введя номер комнаты\n\n"
            "3️⃣ Создатель комнаты может запустить поиск случайных фильмов нажав на «🎲 Случайный подбор» или выбрать жанр для поиска фильмов нажав на «🎭 Выбрать жанр»\n\n"
            "4️⃣ После этого Вам будут предлагать фильмы, а вы их оценивать нажатием на «❤️» или «👎»\n\n"
            "5️⃣ После того как все участники комнаты оценят предложенные им фильмы появится список совпавших фильмов у всех участников комнаты\n\n"
            "6️⃣ Вы можете узнать подробную информацию о фильме, нажав на его номер\n\n"
            "Спасибо, что пользуетесь ДайКинчик💋"
    )
    await message.answer(text, parse_mode="Markdown")

def register_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(roomMenu, F.text == "Поехали! 🚜")
    dp.message.register(cancel, F.text == "🔄 Отмена")
    dp.message.register(help_command, Command("info"))

