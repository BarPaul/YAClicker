import utils.db as db
from re import compile
from utils.payment import generate_payment, get_operation
from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.constants import private, Diamond, CURRENCY, PAYMENT_LINK, CANCEL, unix_to_data, ANSWERS, FIND_DIAMOND

diamond = Router(name="Алмазная часть")

@diamond.callback_query(F.data.regexp(compile(r'buy_gems_(\d+)')))
@private
async def buy_gems(call: CallbackQuery, state: FSMContext):
    await state.set_state(Diamond.amount)
    await call.message.edit_text(f'Курс <b>1 💎</b> = <b>{CURRENCY}</b> RUB\nВ данный момент можно купить от <b>2</b> по <b>15 000</b> 💎\nНапишите какое количество алмазов вам нужно: (или нажмите кнопку "отмена")', reply_markup=CANCEL(call.from_user.id))

@diamond.message(Diamond.amount)
async def diamond_state(message: Message, state: FSMContext):
    if not (message.text.isdigit() and 2 <= int(message.text) <= 15000):
        await state.set_state(Diamond.amount)
        return await message.reply(f'<b>❗ Ошибка</b>\nПопробуйте еще раз написать количество алмазов (от <b>2</b> по <b>15 000</b>)', reply_markup=CANCEL(message.from_user.id, False))
    pay = await generate_payment(message.from_user.id, int(message.text))
    await message.reply('Теперь вы можете оплатить покупку!', reply_markup=PAYMENT_LINK(message.from_user.id, pay.redirected_url))
    if await state.get_state() is None:
        return
    await state.clear()

@diamond.callback_query(F.data.regexp(compile(r'diamond_(\d+)')))
@private
async def check_diamonds(call: CallbackQuery, _):
    user = call.from_user
    payments = await db.get_payments(user.id)
    if not payments:
        await call.message.reply("У вас еще не было платежей 😢", reply_markup=FIND_DIAMOND(user.id))
        await call.message.delete()
        return
    text, last = [], set()
    for uid, unix, amount in payments[:5]:
        status = await get_operation(uid, unix, amount)
        ans = ANSWERS.get(status)
        if status == 'success':
            last.add("Спасибо за вашу поддержку! 💌")
            await db.upd_member(user.id, 'gems', amount)
        if status not in ('failed', 'in_progress'):
            await db.rem_payment(user.id, unix, amount)
        text.append(f'<i>{unix_to_data(unix)}</i> | <a href="tg://user?id={user.id}">{html.quote(user.full_name[:32])}</a> {amount} 💎 {ans}')
    await call.message.reply(f"<b>Последние новые платежи:</b>\n{'\n\n'.join(text)}\n\n{'\n'.join(last) if last else ''}", reply_markup=FIND_DIAMOND(user.id))
    await call.message.delete()

@diamond.callback_query(F.data.regexp(compile(r'cancel_(\d+)')))
@private
async def cancel(call: CallbackQuery, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.clear()
    await call.message.delete()
