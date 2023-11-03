from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6526338938:AAH5fJNLx3iqWqfjwv3z6dF7KREmy1fmOEU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой бот на aiogram.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Список команд: /start, /help")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
