from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

startMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поехали! 🚜")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

roomMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🆕 Создать комнату"),
         KeyboardButton(text="👥 Присоединиться")],  # добавил кнопочки
        [KeyboardButton(text="🔍 Найти фильм")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

preStartMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎲 Случайный подбор"), KeyboardButton(text="🎭 Выбрать жанр")],
        [KeyboardButton(text="🔄 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Хочешь выбрать жанр фильмов?"
)

likeDislikeMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❤️"),
         KeyboardButton(text="👎")],
        [KeyboardButton(text="🚪 Уйти")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

cancelMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

searchMenu = ReplyKeyboardMarkup(  # добавил меню с поиском
    keyboard=[
        [KeyboardButton(text="🚫 Закрыть поиск")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

genreMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Комедия"), KeyboardButton(text="Боевик"), KeyboardButton(text="Ужасы")],
        [KeyboardButton(text="Фантастика"), KeyboardButton(text="Мелодрама"), KeyboardButton(text="Драма")],
        [KeyboardButton(text="🔄 Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выбери жанр"
)

menuForConnectedUsers = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚪 Уйти")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

enterPasswordMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)
