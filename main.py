import logging
import config
import asyncio
from datetime import datetime

# the base aiogram import
from aiogram import Bot, Dispatcher, executor, types
# the import for keyboard
import my_keyboards
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from config import *
from bank import Banker
from scripts import *

logging.basicConfig(level=logging.INFO)

# INIT BOT
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# INIT DATA BASE
db = Banker('db.db')


# !!! COMMANDS !!!
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
            await message.answer('Вы начали следить за своими расходами! ✅\n' +
                                 'Чтобы создать первую запись:\n' + instruction)


@dp.message_handler(commands=['stop'])
async def stopChatting(message: types.Message):
    await message.answer('Вы перестали следить за своими расходами😖\nТеперь даже на проезд не хватит...')
    db.setStatus(message.from_user.id, False)


# !!! TRANSFERS !!!
@dp.message_handler()
async def writeTransfer(message: types.Message):
    if int(message.from_user.id) not in db.userIdList(1):
        await message.answer('Я тебя пока не знаю. Напиши /start, чтобы начать.')

    # Note about value of transfer
    elif isDigit(str(message.text)):
        db.addTransfer(message.from_user.id, float(message.text))
        await message.answer('Выберите категорию:', reply_markup=my_keyboards.category_keyboard)

    # Message about a transfer category
    elif db.getLastTransfer(message.from_user.id)[4] == 'неВыбрано' and (str(message.text) in my_keyboards.category_buttons or str(message.text) in my_keyboards.category_buttons):
        category = str(message.text)
        transfer = db.getLastTransfer(message.from_user.id)
        db.updateTransfer(transfer[0], transfer[1], transfer[2], category, transfer[3])
        await message.answer('Запись создана!', reply_markup=ReplyKeyboardRemove())

    # Wrong message
    else:
        await message.answer('Я не понял тебя или ты сделал что-то не по инструкции😖\n'
                             'Я всего лишь робот 🤖\nПожалуйста, следуй следующим пунктам:\n' + instruction)



'''
# echo message
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
'''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
