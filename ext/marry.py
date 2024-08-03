from re import compile
from utils.db import add_marriage, get_marriages, is_married, divorce
from aiogram import F, types, Router
from utils.constants import MARRIAGE, private, STATUS_MARRY

marry = Router(name='Брачная часть')

@marry.message(F.text.lower().startswith("браки"))
async def marries_list(message: types.Message):
    marries, chat, total_text = dict(), message.chat, ['<b>Браки в этом чате:</b>\n']
    for uid1, uid2, hours in (await get_marriages(chat.id)):
        user, propose = (await chat.get_member(int(uid1))).user, (await chat.get_member(int(uid2))).user
        status = STATUS_MARRY(hours)
        if status not in marries:
            marries[status] = [f'{user.mention_html(user.first_name)} + {propose.mention_html(propose.first_name)} ({hours // 24} дн и {hours % 24} ч)']
            continue
        marries[status].append(f'{user.mention_html(user.first_name)} + {propose.mention_html(propose.first_name)} ({hours // 24} дн и {hours % 24} ч)')
    if len(marries) == 0:
        return await message.reply('\n'.join(total_text + ['Отсутствуют 💔', 'Отвечайте кому-либо "Поженить" и ждите согласия партнера']))
    for status, text in marries.items():
        total_text.extend([f'<b>{status}</b>'] + text)
    await message.reply('\n'.join(total_text))

@marry.message(F.text.lower().startswith("развод"))
async def divorce_command(message: types.Message):
    if await is_married(uid := message.from_user.id):
        await divorce(uid)
        return await message.reply("Ваша пара успешно разведена!")
    await message.reply("Вы не состоите в браке!")

@marry.message(F.text.lower().regexp('(брак|поженить|поженится)+'))
async def marry_command(message: types.Message):
    if message.reply_to_message is None:
        return await message.reply("Ответьте тому с кем хотите поженится!")
    user, propose = message.from_user, message.reply_to_message.from_user
    if user == propose:
       return await message.reply("Самолюбие — это наша первая и последняя ялюбовь\n© <b>О. Уайльд</b>")
    elif propose.is_bot:
        await message.reply("Не понимаю тех, кто хочет подарить куклам души и пытается добиться схожести с людьми. Какой бы прекрасной ни была кукла, это лишь имитация, оболочка без души.\n<b>© Призрак в доспехах 2: Невинность (Ghost in the Shell 2: Innocence)</b>")
        # TODO
        # return
    await message.reply(f"<b>{propose.mention_html(propose.first_name)}</b>, внимание!\n<b>{user.mention_html(user.first_name)}</b> сделал(а) вам предложение руки и сердца!", reply_markup=MARRIAGE(user.id, propose.id))


@marry.callback_query(F.data.regexp(compile(r'(accept|decline)_(\d+)_(\d+)')))
@private
async def button_response(call: types.CallbackQuery):
    do, uid1, uid2 = call.data.split("_")
    user, propose = (await call.message.chat.get_member(int(uid1))).user, (await call.message.chat.get_member(int(uid2))).user
    user_ment, prop_ment = propose.mention_html(propose.first_name)
    
    if call.message.chat.type not in ('group', 'supergroup'):
        return await call.message.reply("Нельзя женится в ЛС!")
    if None in (user, propose):
        return await call.message.reply("Данного пользователя не найдено в чате!")

    if await is_married(uid1):
        return await call.message.reply(f"{user_ment} вы уже в браке!")
    elif await is_married(uid2):
        return await call.message.reply(f"{user_ment} сожалеем, но {prop_ment} уже состоит в браке!")

    if do == "decline":
        await call.message.edit_text(f'{prop_ment} отклонил(а) предложение {user_ment}', reply_markup=None)
    else:
        await call.message.edit_text(f'{prop_ment} принял(а) предложение {user_ment}!\nПоздравдяем!', reply_markup=None)
        await add_marriage(uid1, uid2, call.message.chat.id)
