import asyncio
from createBot import dp, bot
from handlers import registerHandlers


async def main():
    registerHandlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
