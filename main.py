import logging
import config
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types

from config import API_TOKEN
from bank import Banker

logging.basicConfig(level=logging.INFO)

# INIT BOT
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# INIT DATA BASE
db = Banker('db.db')


@dp.message_handler(commands=['start'])
async def startChatting(message: types.Message):
    if message.from_user.id in db.userIdList(1):
        await message.answer('Вы уже следите за своими расходами!')
    else:
        if message.from_user.id in db.userIdList(0):
            db.setStatus(message.from_user.id, True)
            await message.answer('Вы снова следите за своими финансами!✅')
        else:
            db.addUser(message.from_user.id)
            await message.answer('Вы начали следить за своими расходами! ✅\n'
                                 'Чтобы совздать первую запись:\n1) Выберите пришли или ушли деньги 💸\n'
                                 '2) Введите сумму ↕\n3) Выберите категорию📃')


@dp.message_handler(commands=['stop'])
async def stopChatting(message: types.Message):
    await message.answer('Вы перестали следить за своими расходами😖\nТеперь даже на проезд не хватит...')
    db.setStatus(message.from_user.id, False)


'''
# echo message
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
'''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
