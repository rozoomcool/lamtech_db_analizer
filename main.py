import asyncio

from aiogram import Bot, Dispatcher, executor, types
import psycopg2
import db
import users
import dbscript
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    types.InlineKeyboardButton(text='Проверить работу сервера'),
    types.InlineKeyboardButton(text='Производительность'),
    types.InlineKeyboardButton(text='Статистика запросов')
)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db.create_user(message.from_user.id)
    await message.reply("Привет! Я твой бот на aiogram.", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Список команд: /start, /help", reply_markup=keyboard)


@dp.message_handler(commands=['check'])
async def check_bd(message: types.Message):
    try:
        conn = psycopg2.connect(
            host="5.53.124.214",
            port = "5432",
            database="lamtech_db",
            user="postgres",
            password="root"
        )
        await message.answer("Сервер работает в штатном режиме", reply_markup=keyboard)
    except Exception as e:
        print(e)
        await message.answer("База данных не работает", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Проверить работу сервера')
async def send_welcome(message: types.Message):
    await check_bd(message)


@dp.message_handler(lambda message: message.text == 'Статистика запросов')
async def send_welcome(message: types.Message):
    await users.send_message(bot, 'Статистика')


@dp.message_handler(lambda message: message.text == 'Производительность')
async def send_welcome(message: types.Message):
    
    await message.reply("Быстро", reply_markup=keyboard)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


async def db_ok():
    await users.send_message(bot, 'OK')


async def db_failed():
    await users.send_message(bot, 'Внимание сука! Произошел сбой в работе базы данных:')

async def check_db_exec(_):
    asyncio.create_task(dbscript.checking_db(db_ok, db_failed))

def main():
    executor.start_polling(dp, skip_updates=True, on_startup=check_db_exec)

if __name__ == '__main__':
    main()
