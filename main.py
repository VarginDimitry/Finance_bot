import logging
import config
import asyncio
from datetime import datetime

from aiogram import  Bot, Dispatcher, executor, types

from config import API_TOKEN
from bank import Banker

logging.basicConfig(level=logging.INFO)

# INIT BOT
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# INIT DATA BASE
db = Banker('db.db')


'''
# echo message
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
'''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)