from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp


@dp.message_handler(F.text == "📞 Aloqa")
async def contact_info(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "📲 Biz bilan bog‘lanish uchun:\n"
        "Telefon: +998 90 123 45 67\n"
        "Instagram: @bizniklinika\n"
        "Telegram: @bizniklinika_bot"
    )
