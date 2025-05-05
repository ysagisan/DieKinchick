from aiogram.types import BotCommand

async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(command="/info", description="Что может этот бот")
    ]
    await bot.set_my_commands(commands)
