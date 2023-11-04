from aiogram import Bot, Dispatcher, executor, types
import psycopg2
import db
import users
import dbscript
from background_process import BackgroundProcess

import config


bot = Bot(token=config.TOKEN)
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
    await bot.send_message("База данных работает отлично")


async def db_failed():
    await bot.send_message("Внимание сука! Произошел сбой в работе базы данных:")


async def run():
    executor.start_polling(dp, skip_updates=True)

def run_db_checking():
    dbscript.checking_db(db_ok, db_failed)



if __name__ == '__main__':
    run_db_checking()
    executor.start_polling(dp, skip_updates=True)
