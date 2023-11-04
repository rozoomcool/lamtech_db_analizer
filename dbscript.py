from time import sleep

import asyncpg


async def check_db(on_ok=None, on_failed=None):
    try:
        conn = await asyncpg.connect(
            host="5.53.124.214",
            port="5432",
            database="lamtech_db",
            user="postgres",
            password="root"
        )

        await conn.executed("SELECT * FROM pg_stat_activity;")
        await conn.close()

        await on_ok()
        return True
        # await bot.send_message("База данных работает отлично")

    except (asyncpg.PostgresError, ConnectionError) as e:
        await on_failed()
        return False
        # await bot.send_message("Произошел сбой в работе базы данных:", e)


async def checking_db(on_ok, on_failed):
    print('[dbscript] start checking')
    while True:
        sleep(2)
        print('[dbscript] cheeeck')
        await check_db(on_ok, on_failed)


def status(update,  context):
    db_status = check_db()
    update.message.reply_text(f"[dbscript] Current DB status: {db_status}")
