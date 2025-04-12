# from aiogram import F, Dispatcher
# from aiogram.filters import CommandStart
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message
# from botSettings.createBot import dp
#
#
# @dp.message(F.text == "❤️")
# async def like(message: Message):
#     pass
#
# @dp.message(F.text == "👎")
# async def dislike(message: Message):
#     pass
#
# def register_handlers(dp: Dispatcher):
#     dp.message.register(like, F.text == "❤️")
#     dp.message.register(dislike, F.text == "👎")
