from typing import Any, Literal, List, Union
from dataclasses import dataclass
from aiosqlite import connect
from asyncio import run

async def __execute(query: str, args: tuple = None, fetchall: bool = False) -> Any:
    async with connect('utils/database.db') as db:
        execute_args = (query,) if args is None else (query, args,)
        async with db.execute(*execute_args) as cursor:
            res = await cursor.fetchall() if fetchall else await cursor.fetchone()
        await db.commit()    
    return res

@dataclass
class Member:
    id: int
    money: int
    gems: int

async def add_member(uid: int):
    await __execute("INSERT INTO users VALUES (?, ?, ?)", (uid, 0, 0,))

async def get_member(uid: int) -> Union[Member, bool]:
    res = await __execute('SELECT * FROM users WHERE id = ?', (uid,))
    if res is None:
        return False
    return Member(*res)

async def rem_member(uid: int):
    await __execute("DELETE FROM users WHERE id = ?", (uid,))

async def upd_member(uid: int, update_type: Literal["money", "gems", "money, gems"], *values: List[int]):
    query_part = ', '.join([f"{name} = {name} + {value}" for name, value in zip(update_type.split(", "), values)])
    await __execute(f"UPDATE users SET {query_part} WHERE id = ?", (uid,))
    member = await get_member(uid)
    if member.money < 0:
        await upd_member(uid, 'money', -member.money)
    if member.gems < 0:
        await upd_member(uid, 'gems', -member.gems)

async def add_timer(uid: int, time: int, event: str):
    await __execute('INSERT INTO timers VALUES (?, strftime(\'%s\', \'now\') + ?, ?)', (uid, time, event,))

async def get_timer(uid: int, event: str):
    return await __execute('SELECT unix <= strftime(\'%s\', \'now\') FROM timers WHERE id = ? AND event = ?', (uid, event,))

async def rem_timer(uid: int, event: str):
    await __execute("DELETE FROM timers WHERE id = ? AND event = ?", (uid, event,))

async def add_payment(uid: int, _, diamonds: int):
    await __execute("INSERT INTO payments VALUES (?, strftime(\'%s\', \'now\') , ?)", (uid, diamonds,))

async def rem_payment(uid: int, unix: int, diamonds: int):
    await __execute("DELETE FROM payments WHERE id = ? AND unix = ? AND diamonds = ?", (uid, unix, diamonds,))

async def get_payments(uid: int) -> list:
    return list(await __execute("SELECT * FROM payments WHERE id = ?", (uid,), fetchall=True))

async def main():
    await __execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY NOT NULL,
    money INTEGER NOT NULL,
    gems INTEGER NOT NULL)''')
    await __execute('''CREATE TABLE IF NOT EXISTS timers (
    id INTEGER NOT NULL,
    unix INTEGER NOT NULL,
    event TEXT NOT NULL)''')
    await __execute('''CREATE TABLE IF NOT EXISTS payments (
    id INTEGER NOT NULL,
    unix INTEGER NOT NULL,
    diamonds INTEGER NOT NULL)''')


if __name__ == '__main__':
    run(main())
