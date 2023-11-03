from aiogram import Bot, Dispatcher, executor, types

import config


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой бот на aiogram.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Список команд: /start, /help")


@dp.message_handler()
async def echo(message: types.Message):

    if 'росул' in message.text.lower():
        await message.answer('Понятно, недопроггер значит.')
        return

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
