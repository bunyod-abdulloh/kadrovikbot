from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp


@dp.message_handler(F.text == "🌐 Tilni o‘zgartirish", state="*")
async def change_language(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "🌐 Iltimos, tilni tanlang:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton("🇺🇿 O‘zbek"), types.KeyboardButton("🇷🇺 Русский")],
                [types.KeyboardButton("🇬🇧 English")],
                [types.KeyboardButton("⬅️ Ortga")]
            ],
            resize_keyboard=True
        )
    )
