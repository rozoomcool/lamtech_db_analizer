from aiogram import Bot
import db

async def send_message(bot: Bot, message: str):
    for user_id in db.get_all_user_ids():
        await bot.send_message(user_id, message)

