from re import compile
from db import get_member, add_member
from constants import FIND_DIAMOND, MENU
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram import F, html, types, Router

start = Router(name='Стартовая часть')

@start.message(CommandStart(deep_link=True, magic=F.args.regexp(compile(r'payment_(\d+)'))))
async def payment_event(message: types.Message, command: CommandObject):
    await message.reply(f'Ожидайте пополнения в 💎 {command.args.split("_")[-1]}!', reply_markup=FIND_DIAMOND(message.from_user.id))

@start.message(Command('start'))
async def start_command(message: types.Message):
    uid = message.from_user.id
    member = await get_member(uid)
    if not member:
        await message.answer(f'Привет! Ты успешно получил своего питомца, <b>Яка</b>!')
        await add_member(uid)
    else:
        await message.answer(f'🐂 <b><a href="tg://user?id={uid}">{html.quote(message.from_user.full_name[:32])}</a></b>\n💰 <b>{member.money}</b>\n💎 <b>{member.gems}</b>', reply_markup=MENU(message.from_user.id))
