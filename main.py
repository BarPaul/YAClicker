from utils.constants import TOKEN
from ext import ROUTERS
from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from asyncio import run


bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()


async def main():
    basicConfig(level=INFO, format="%(asctime)s %(levelname)s | %(message)s", datefmt="%d.%m.%y %H:%M")
    dp.include_routers(*ROUTERS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
