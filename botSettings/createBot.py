import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import os

logging.basicConfig(level=logging.INFO)
load_dotenv()
bot = Bot(os.getenv("TOKEN"))  # Bot(token=token)
dp = Dispatcher()
