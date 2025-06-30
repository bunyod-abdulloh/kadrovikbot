from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from magic_filter import F

from keyboards.default.users_dkb import main_menu_cb
from loader import dp, udb


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await udb.add_user(telegram_id=message.from_user.id)

    await message.answer(text=f"👋 Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n\n"
                              "🎉 Botimizga xush kelibsiz!", reply_markup=main_menu_cb)


@dp.message_handler(F.text == "⬅️ Ortga", state="*")
async def handle_back_button(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=message.text, reply_markup=main_menu_cb
    )
