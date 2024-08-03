from aiogram.types import InlineKeyboardMarkup as InlineMarkup, InlineKeyboardButton as InlineButton, CallbackQuery, Message
from aiogram.filters.state import State, StatesGroup
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

ADMIN_IDS = (1843313209,)

class Diamond(StatesGroup):
    amount = State()

def private(func):
    async def wrapper(call: CallbackQuery, state = None):
        if int(call.data.split("_")[-1]) != call.from_user.id:
            await call.answer('Не твое - не трогай!')
            return
        return await func(call) if state is None else await func(call, state)
    return wrapper

def admin_filter(func):
    async def wrapper(message: Message):
        if not message.from_user.id in ADMIN_IDS:
            await message.answer('Это команда для админов!', True)
            return
        res = await func(message)
        await message.delete()
        return res
    return wrapper

TOKEN, CURRENCY = getenv("TOKEN"), getenv("DIAMOND_RUB")
MENU = lambda uid: InlineMarkup(inline_keyboard=[
    [InlineButton(text='🌽 Фармить', callback_data=f'earn_money_{uid}')], 
    [InlineButton(text='💎 Купить', callback_data=f'buy_gems_{uid}')]
])
FIND_DIAMOND = lambda uid: InlineMarkup(inline_keyboard=[[InlineButton(text='💎 Проверить', callback_data=f'diamond_{uid}')]])
CANCEL = lambda uid, with_check = True: InlineMarkup(inline_keyboard=[
    [InlineButton(text='📋 Проверить', callback_data=f'diamond_{uid}')] if with_check else [],
    [InlineButton(text='❌ Отмена', callback_data=f'cancel_{uid}')]
])
PAYMENT_LINK = lambda uid, url: InlineMarkup(inline_keyboard=[
    [InlineButton(text='💵 Оплатить', url=url)],
    [InlineButton(text='📋 Проверить', callback_data=f'diamond_{uid}')]
])
unix_to_data = lambda unix: datetime.fromtimestamp(unix).strftime("%d.%m.%Y %H:%M:%S")
ANSWERS =  {
    'success': 'Заказ получен 💘',
    'refused': 'Заказ отменен 💔',
    'in_progress': 'Принимается оплата 🎁',
    'failed': 'Заказ в обработке. ⌛'
}
MARRIAGE = lambda uid1, uid2: InlineMarkup(inline_keyboard=[
    [InlineButton(text="✅ Принять", callback_data=f"accept_{uid1}_{uid2}"), InlineButton(text="💔 Отклонить", callback_data=f"decline_{uid1}_{uid2}")]
])
STATUS_MARRY = lambda hours: {
    0 <= hours < 31 * 24: "💍 Молодожены",
    31 * 24 <= hours < 2 * 31 * 24: "🎁 Секретная годовщина",
    2 * 31 * 24 <= hours < 3 * 31 * 24: "🌽 Кукурузная годовщина",
    3 * 31 * 24 <= hours < 6 * 31 * 24: "🥇 Золотая годовщина",
    6 * 31 * 24 <= hours < 12 * 31 * 24: "💎 Алмазная годовщина",
    12 * 31 * 24 <= hours < 24 * 31 * 24: "💖 Любовная годовщина",
    24 * 31 * 24 <= hours: "💘 Божественная любовь"
}.get(True, "Error")