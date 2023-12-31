import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import psycopg2
import db
import users
import dbscript
import psutil
from dotenv import dotenv_values
import bench_requests
import analyzer.slow_query
import logs.logs
import utils.backup
import charts.generator

# TODO: errors handler

config = dotenv_values(".env")


bot = Bot(token=config['TOKEN'])
dp = Dispatcher(bot)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    types.InlineKeyboardButton(text='Проверить работу БД'),
    types.InlineKeyboardButton(text='Информация о системе'),
    types.InlineKeyboardButton(text='Перезагрузить БД'),
    types.InlineKeyboardButton(text='Получить логи'),
    types.InlineKeyboardButton(text='Сгенерировать графики'),
    types.InlineKeyboardButton(text='Тестирование'),
    types.InlineKeyboardButton(text='Проверить время выполнения запросов'),
    types.InlineKeyboardButton(text='Сделать бэкап бд'),
    types.InlineKeyboardButton(text='Востановить бд из бэкапа'),
)


class Form(StatesGroup):
    scaleFactor = State()
    clients = State()
    threads = State()
    seconds = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db.create_user(message.from_user.id)
    await message.reply("Добро пожаловать.", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Список команд: /start, /help", reply_markup=keyboard)


@dp.message_handler(commands=['check'])
async def check_bd(message: types.Message):
    try:
        conn = psycopg2.connect(
            host="5.53.124.214",
            port="5432",
            database="lamtech_db",
            user="postgres",
            password="root"
        )
        await message.answer("БД работает в штатном режиме", reply_markup=keyboard)
    except Exception as e:
        print(e)
        await message.answer("БД не отвечает", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Проверить работу БД')
async def check_server(message: types.Message):
    await check_bd(message)


@dp.message_handler(lambda message: message.text == 'Перезагрузить БД')
async def restart_db_btn(message: types.Message):
    await users.send_message(bot, 'БД перезагружается, ждите')
    if(bench_requests.restart_db() != 200):
        await message.answer('Произошла непредвиденная ошибка')
    else:
        await message.answer('БД перезагружена')


@dp.message_handler(lambda message: message.text == 'Информация о системе')
async def server_info(message: types.Message):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    partitions = psutil.disk_partitions()
    net_io = psutil.net_io_counters()

    sys_message = f"Загрузка ЦПУ: {cpu_usage}% \n\n"
    sys_message += f'Объем ОЗУ: {memory.total / (1024 ** 2):.2f} MB\nИспользуеммая память: {memory.used / (1024 ** 2):.2f} MB\nСвободная память: {memory.free / (1024 ** 2):.2f} MB\n\n'

    for part in partitions:
        usage = psutil.disk_usage(part.mountpoint)
        sys_message += f'Раздел: {part.device}\n'
        sys_message += f"\tОбъем: {usage.total / (1024 ** 3):.2f} GB\n\tИспользовано: {usage.used / (1024 ** 3):.2f} GB\n\tСвободно: {usage.free / (1024 ** 3):.2f} GB"

    await message.answer(sys_message, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Получить логи')
async def logs_btn(message: types.Message):
    file = logs.logs.gen_logs()
    with open (f"./{file}", "rb") as log_file:
        await bot.send_document(chat_id=message.chat.id, document=log_file)


@dp.message_handler(lambda message: message.text == 'Сгенерировать графики')
async def chart_btn(message: types.Message):
    charts.generator.get_general(charts.generator.get_conn())
    charts.generator.get_tables_stat(charts.generator.get_conn())
    charts.generator.get_indexes_stat(charts.generator.get_conn())

    gen_charts = [
        'Занятое_и_свободное_пространство_в_базе_данных.png',
        'количества_сканирований_таблиц_(seq_scan)_и_записей_таблиц.png',
        'статистики_по_индексам.png'
    ]

    await message.answer('Начинаю генерировать графики...')
    for chart in gen_charts:
        with open (f"./charts/{chart}", "rb") as chart:
            await bot.send_document(chat_id=message.chat.id, document=chart)


@dp.message_handler(lambda message: message.text == 'Тестирование')
async def easy_test_btn(message: types.Message):
    await message.answer('Начинаю нагрузочный тест...')
    data = bench_requests.easy_test()
    if(data['status'] != 200):
        await message.answer('Произошла непредвиденная ошибка')
    else:
        await message.answer('Результат выполнения теста: ')
        params = ''
        for param in data['data']:
            params += param + '\n'
        await message.answer(params)


@dp.message_handler(lambda message: message.text == 'Проверить время выполнения запросов')
async def hard_test_btn(message: types.Message):
    await message.answer('Начинаю сбор информации...')
    data = analyzer.slow_query.get_tables_list(analyzer.slow_query.get_conn())
    res = analyzer.slow_query.check_query_time(analyzer.slow_query.get_conn(), data)
    for table in res:
        query_execute_time = 'Медленно' if float(res[table]['execution_time']) >= 2 else 'Быстро' # итоговая оценка скорость выполнения запроса
        await message.answer(f"Таблица: {table} \n Запрос: ```sql f{res[table]['executed_query']} ``` \n Ожидаемое время выполнения запроса: {res[table]['planning_time']} мл \n Время выполнения запроса: {res[table]['execution_time']} мл \n Итоговая оценка скорость выполнения запроса(время в 2 миллисекунды используются для примера): {query_execute_time}")


@dp.message_handler(lambda message: message.text == 'Сделать бэкап бд')
async def backup_btn(message: types.Message):
    await message.answer('Начинаю бэкап...')
    r = utils.backup.backup_db()
    await message.answer(r)

@dp.message_handler(lambda message: message.text == 'Востановить бд из бэкапа')
async def restore_btn(message: types.Message):
    await message.answer('Начинаю восстановление...')
    r = utils.backup.restore_db()
    await message.answer(r)

async def db_ok():
    await users.send_message(bot, 'База данных работает в штатном режиме')

async def db_failed():
    await users.send_message(bot, 'Внимание! Произошел сбой в работе базы данных:')

async def check_db_exec(_):
    asyncio.create_task(dbscript.checking_db(db_ok, db_failed))


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=check_db_exec)


if __name__ == '__main__':
    main()
