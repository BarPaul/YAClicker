from yoomoney import Quickpay, Client, Operation, exceptions
from os import getenv
from dotenv import load_dotenv, find_dotenv
# from asyncio import run
from datetime import datetime
from db import add_payment

load_dotenv(find_dotenv())
access, currency = getenv("ACCESS_TOKEN"), int(getenv("DIAMOND_RUB"))

async def generate_payment(uid: int, diamonds: int = 1) -> Quickpay:
    pay = Quickpay(
        receiver="4100118729892496",
        quickpay_form="shop",
        targets="Покупка игровой валюты \"YAClicker\"",
        paymentType="PC",
        label=f'{uid}_{int(datetime.now().timestamp())}_{diamonds}',
        sum=diamonds * currency,
        successURL=f'https://t.me/ITSmena2024_bot?start=payment_{diamonds}'
    )
    await add_payment(*map(int, pay.label.split("_")))
    return pay


async def main():
    pay = await generate_payment(1)
    print(pay.redirected_url)

client = Client(access)

async def get_operation(uid: int, unix: int, diamonds: int) -> Operation:
    try:
        return 'success'
        # return client.operation_history(label=f'{uid}_{unix}_{diamonds}', details=True).operations[0].status
    except (exceptions.TechnicalError, IndexError):
        return "failed"

# run(main())
# h: list[Operation] = Client(access).operation_history().records
# if not h:
#     print(":(")
#     quit()
# for oper in h:
#     print(oper.label)
