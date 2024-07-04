import db
from re import compile
from constants import *
from ext import diamond, admin
from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, CallbackQuery
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command, CommandStart, CommandObject

basicConfig(level=INFO, format="%(asctime)s %(levelname)s | %(message)s", datefmt="%d.%m.%y %H:%M")

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()

@dp.message(CommandStart(deep_link=True, magic=F.args.regexp(compile(r'payment_(\d+)'))))
async def payment_event(message: Message, command: CommandObject):
    await message.reply(f'Ожидайте пополнения в 💎 {command.args.split("_")[-1]}!', reply_markup=FIND_DIAMOND(message.from_user.id))

@dp.message(Command('start'))
async def start_command(message: Message):
    member = await db.get_member(message.from_user.id)
    if not member:
        await message.reply(f'Привет! Ты успешно получил своего питомца, <b>Яка</b>!')
        await db.add_member(message.from_user.id)
    else:
        await message.reply(f'🐂 <b><a href="tg://user?id={message.from_user.id}">{html.quote(message.from_user.full_name[:32])}</a></b>\n💰 <b>{member.money}</b>\n💎 <b>{member.gems}</b>', reply_markup=MENU(message.from_user.id))

@dp.callback_query(F.data.regexp(compile(r'earn_money_(\d+)')))
@private
async def earn_money(call: CallbackQuery):
    await call.answer(f'{call.from_user.full_name} пытался заработать деньги!', True)


async def main():
    dp.include_routers(diamond.diamond, admin.admin)
    await dp.start_polling(bot)


if __name__ == "__main__":
    db.run(main())
