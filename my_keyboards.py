from config import *

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# TRANSFERS CATEGORY KEYBOARD
category_buttons = [x+'➕' for x in plus_category] + \
                   [x+'➖' for x in minus_category] + \
                   [x + '✖' for x in neutral_category]
map(KeyboardButton, category_buttons)
category_keyboard = ReplyKeyboardMarkup()
for i in range(len(category_buttons)):
    category_keyboard.add(category_buttons[i])