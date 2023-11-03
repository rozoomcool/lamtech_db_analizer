import time

import asyncpg

async def checking_db():
    while True:
        await sleep(1000 * 60)
        await check_db()

        async def check_db():
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
                await bot.send_message("База данных работает отлично")

            except (asyncpg.PostgresError, ConnectionError) as e:
                await bot.send_message("Произошел сбой в работе базы данных:", e)


def status(update,  context):
    db_status = check_db()
    update.message.reply_text(f"Current DB status: {db_status}")