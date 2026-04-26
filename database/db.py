import aiosqlite as sq
from aiogram import types
async def check_me(user_id, response_text, data, message:types.Message):
    async with sq.connect('users.db') as con:

            await con.execute("""
    CREATE TABLE IF NOT EXISTS users_profile(
                        user_id INTEGER,
                        name TEXT,
                        age INTEGER,
                        purpose TEXT
                        )
                        """)
            async with con.execute(f"SELECT * FROM users_profile WHERE user_id == ?", (user_id,)) as cursor:
                user = await cursor.fetchone()
                
            if user:
                await con.execute(
                "UPDATE users_profile SET name = ?, age = ?, purpose = ? WHERE user_id = ?",
                (data["name"], data['age'], data['purpose'], user_id))
                await message.answer('Your info was changed')
                await message.answer(response_text)
            else:
                await con.execute(
                "INSERT INTO users_profile VALUES(?, ?, ?, ?)",
                (user_id, data['name'], data['age'], data['purpose']))
                await message.answer(response_text)
            await con.commit()

async def found_me(user_id, message:types.Message):
    async with sq.connect('users.db') as con:
        async with con.execute(f"SELECT * FROM users_profile WHERE user_id == ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
        if user:
            name = user[1]
            age = user[2]
            purpose = user[3]
            await message.answer(f"Username : {user_id}.\nName : {name}.\nAge : {age}.\nPurpose : {purpose}")
        else:
            await message.answer("Sorry but we havent found")