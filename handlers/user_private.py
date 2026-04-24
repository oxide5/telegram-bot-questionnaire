import sqlite3 as sq
from aiogram import F, types, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os
from kbds import reply
from dotenv import find_dotenv, load_dotenv

ADMIN_ID = os.getenv("ADMIN_ID")

ro = Router()



class Profile(StatesGroup):
    name = State()
    age = State()
    purpose = State()


@ro.message(CommandStart())
async def start_cmd(message:types.Message):
    await message.answer("Hello! Im a profile bot, i will send your name, age, purpose of the visit to my creater. Do you want to continue?\nTap \'yes\' to start, \'no\' to refuse", reply_markup=reply.start_kb)
    
@ro.message(F.text.lower() == "yes")
async def start_survey(message: types.Message, state: FSMContext):
    await message.answer("Okay, enter your name:", reply_markup=reply.del_kb)
    await state.set_state(Profile.name)



@ro.message(Profile.name)
async def get_name(message: types.Message, state: FSMContext):
    if message.photo or message.text.isdigit():
        await message.answer("You can't add photo or numbers as your name")
        return
    else:
        await state.update_data(name=message.text)
        await message.answer(f"Nice to meet you, {message.text}! Now enter your age:", reply_markup=reply.keyboard_name )
        await state.set_state(Profile.age)

@ro.callback_query(F.data == "back_to_name")
async def back_to_step1(callback: CallbackQuery, state: FSMContext):    
    await state.set_state(Profile.name)
    await callback.message.edit_text("Enter your new name")

@ro.message(Profile.age)
async def get_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or message.photo:
        await message.answer("Please enter only numbers")
        return 
    age = int(message.text)

    if age < 1 or age > 120:
        await message.answer("Your age cant be less than 1 or more than 120. Try again")
    else:
        await state.update_data(age=age)
        await message.answer("The last one: What is your purpose of the visit?", reply_markup=reply.keyboard_age)
        await state.set_state(Profile.purpose)

@ro.callback_query(F.data == "back_to_age")
async def back_to_step2(callback: CallbackQuery, state: FSMContext):    
    await state.set_state(Profile.age)
    await callback.message.edit_text("Enter your new age")

@ro.message(Profile.purpose)
async def get_purpose(message: types.Message, state: FSMContext, bot: Bot):
    if message.photo or message.text.isdigit():
        await message.answer("You can't add photo or numbers as your name")
        return
    else:
        await state.update_data(purpose=message.text)

        data = await state.get_data()

        user_id = message.from_user.id


        response_text = (
            f"The questionnaire is completed!\n"
            f"Account: {user_id}\n"
            f"Name: {data['name']}\n"
            f"Age: {data['age']}\n"
            f"Purpose: {data['purpose']}"
        )

        await bot.send_message(chat_id=ADMIN_ID,   #send to admin
            text = 
            f"Account: {user_id}\n"
            f"Name: {data['name']}\n"
            f"Age: {data['age']}\n"
            f"Purpose: {data['purpose']}")



        with sq.connect('users.db') as con:
            cur = con.cursor()
            cur.execute("""
    CREATE TABLE IF NOT EXISTS users_profile(
                        user_id INTEGER,
                        name TEXT,
                        age INTEGER,
                        purpose TEXT
                        )
                        """)
            cur.execute(f"SELECT * FROM users_profile WHERE user_id == ?", (user_id,))
            user = cur.fetchone()
            if user:
                change = "UPDATE users_profile SET name = ?, age = ?, purpose = ? WHERE user_id = ?"
                cur.execute(change, (data["name"], data['age'], data['purpose'], user_id))
                await message.answer('Your info was changed')
                await message.answer(response_text)
                con.commit()
            else:
                data_info = "INSERT INTO users_profile VALUES(?, ?, ?, ?)"
                cur.execute(data_info, (user_id, data['name'], data['age'], data['purpose']))
                await message.answer(response_text)
                con.commit()

        await state.clear()



@ro.message(F.text.lower() == "no")
async def info_user(message:types.Message):
    await message.answer("Okay, if u change your mind send /start", reply_markup= reply.del_kb)


@ro.message(Command('about_me'))
async def about_me(message: types.Message):
    user_id = message.from_user.id
    with sq.connect('users.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users_profile WHERE user_id == ?", (user_id,))
        user = cur.fetchone()
        if user:
            name = user[1]
            age = user[2]
            purpose = user[3]
            await message.answer(f"Username : {user_id}.\nName : {name}.\nAge : {age}.\nPurpose : {purpose}")
        else:
            await message.answer("Sorry but we havent found")