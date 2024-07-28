from re import compile
from db import add_timer, get_timer, rem_timer
from aiogram import F, types, Router
from constants import private

money = Router('Денежная часть')

@money.callback_query(F.data.regexp(compile(r'earn_money_(\d+)')))
@private
async def earn_money(call: types.CallbackQuery, _ = None):
    uid = call.from_user.id
    timer = await get_timer(uid, 'earn_money')
    if timer is None:
        await call.message.reply("Отправляемся на прогулку!\nПриходи через час")
        await add_timer(uid, 60, 'earn_money')
    elif timer[0]:
        await call.message.reply("Прогулка окончена! Так как это тест, ты еще ничего не получишь")
        await rem_timer(uid, 'earn_money')
    else:
        await call.answer("Прогулка еще не окончена!")
