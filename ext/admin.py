from utils.db import upd_member
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message
from utils.constants import admin_filter


admin = Router(name="Админская часть")


@admin.message(Command(commands=['add_money', 'rem_money', 'add_gems', 'rem_gems']))
@admin_filter
async def change_economy(message: Message):
    reply = message.reply_to_message
    if reply is None:
        return await message.reply('Ответьте на чье либо сообщение, чтобы добавить ему монет!')
    command, *amount = message.text.split()
    if len(amount) != 1 or not amount[0].isdigit() or int(amount[0]) <= 0:
        return await message.reply(f'{command} {html.quote("<количество_валюты>")} (больше 0)\n<b>Пример команды:</b>\n{command} 152')
    ratio, what = command[1:].split("_")
    await upd_member(reply.from_user.id, what, {'add': 1}.get(ratio, -1) * int(amount[0]))
    await message.reply(f'Пользователю <a href="tg://user?id={reply.from_user.id}">{html.quote(reply.from_user.full_name[:32])}</a>\
 {"выдано" if ratio == 'add' else "отнято"} {amount[0]} {"🌽" if what == 'money' else "💎"}')
