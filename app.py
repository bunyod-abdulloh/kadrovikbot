import middlewares, filters, handlers

from aiogram import executor

from loader import dp, db, kdb
from services.notify_admins import on_startup_notify
from services.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await db.create()
    # await db.drop_table_links()
    # await db.drop_table_users()
    # await kdb.drop_table_employee()
    await db.create_tables()
    # await db.add_send_status()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
