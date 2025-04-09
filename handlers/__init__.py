from handlers import handlers
from aiogram.filters import CommandStart
from handlers import handlers as hd
from aiogram import F


import importlib
from pathlib import Path
from aiogram import Dispatcher


def registerHandlers(dp: Dispatcher):
    # Получаем список всех файлов-хендлеров в папке handlers
    handler_files = [f.stem for f in Path(__file__).parent.glob("*.py") if f.is_file() and f.stem != "__init__"]

    for module_name in handler_files:
        # Динамически импортируем модуль
        module = importlib.import_module(f"handlers.{module_name}")

        # Если в модуле есть функция register_handlers, вызываем её
        if hasattr(module, "register_handlers"):
            module.register_handlers(dp)