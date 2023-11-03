import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import config


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token(os.environ['TOKEN']).build()

app.add_handler(CommandHandler("start", hello))

app.run_polling()
