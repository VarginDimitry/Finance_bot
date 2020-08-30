from config import *

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# TRANSFERS CATEGORY KEYBOARD
category_buttons = [x+'➕' for x in plus_category] + \
                   [x+'➖' for x in minus_category]

map(KeyboardButton, category_buttons)
category_keyboard = ReplyKeyboardMarkup()
category_counter = len(category_buttons)
if category_counter % 2 == 0:
    for i in range(0, category_counter, 2):
        category_keyboard.row(category_buttons[i], category_buttons[i+1])
else:
    for i in range(0, category_counter-1, 2):
        category_keyboard.row(category_buttons[i], category_buttons[i+1])
    category_keyboard.add(category_buttons[category_counter-1])