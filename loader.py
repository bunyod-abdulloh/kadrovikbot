from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.kadrovik import KadrovikDB
from utils.db_api.main_db import Database
from utils.db_api.users_admins import UsersAdminsDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersAdminsDB(db)
kdb = KadrovikDB(db)
