import asyncio
from createBot import dp, bot
from handlers import registerHandlers
from handlers.setCommands import set_commands


async def main():
    registerHandlers(dp)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
