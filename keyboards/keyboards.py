from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

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
        [KeyboardButton(text="Создать комнату"),
         KeyboardButton(text="Подключиться к комнате"),  # добавил кнопочки
         ],
        [KeyboardButton(text="Найти фильм"),
         KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

preStartMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать подбор фильма"),
         KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

likeDislikeMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❤️"),
         KeyboardButton(text="👎"),
         KeyboardButton(text="Уйти")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

cancelMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)

searchMenu = ReplyKeyboardMarkup(  # добавил меню с поиском
    keyboard=[
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Ну что погнали нафиг"
)
