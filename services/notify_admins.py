import logging

from aiogram import Dispatcher

from data.config import ADMIN_GROUP, ADMINS


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMINS[0], "Bot ishga tushdi")

    except Exception as err:
        logging.exception(err)
