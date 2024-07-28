from constants import TOKEN
from ext import diamond, admin, start, money
from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties


bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()


async def main():
    basicConfig(level=INFO, format="%(asctime)s %(levelname)s | %(message)s", datefmt="%d.%m.%y %H:%M")
    dp.include_routers(diamond.diamond, admin.admin, start.start, money.money)
    await dp.start_polling(bot)


if __name__ == "__main__":
    db.run(main())
