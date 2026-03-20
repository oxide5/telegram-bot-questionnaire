from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Yes'),
            KeyboardButton(text='No'),
        ],
    ],
    resize_keyboard=True,
)


del_kb = ReplyKeyboardRemove()

back_to_name = InlineKeyboardButton(text="Back", callback_data='back_to_name')
back_to_age = InlineKeyboardButton(text="Back", callback_data='back_to_age')

keyboard_name = InlineKeyboardMarkup(inline_keyboard=[[back_to_name]], resize_keyboard=True)
keyboard_age = InlineKeyboardMarkup(inline_keyboard=[[back_to_age]], resize_keyboard=True)