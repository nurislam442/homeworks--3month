from config import bot, dp, Admins
from aiogram import executor
import logging
from handlers import commands, quiz, echo, store, send_products, send_and_delete_products, edit_products

from db import db_main


async def on_startup(_):
    for i in Admins:
        await bot.send_message(chat_id=i, text='бот активирован!')
        await db_main.sql_create()
async def on_shutdown(_):
    for i in Admins:
        await bot.send_message(chat_id=i, text="бот выключен")


commands.register_commands(dp)
quiz.register_handler_quiz(dp)
store.reg_handler_fsm_registration(dp)
store.reg_handler_fsm_store(dp)


commands.register_commands(dp)
quiz.register_handler_quiz(dp)
store.reg_handler_fsm_registration(dp)

send_products.register_handlers(dp)
send_and_delete_products.register_handlers(dp)

edit_products.register_edit_handler(dp)

echo.register_echo_handler(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, allowed_updates=['callback'], on_startup=on_startup, on_shutdown=on_shutdown)
