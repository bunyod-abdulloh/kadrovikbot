from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp


@dp.message_handler(F.text == "ℹ️ Biz haqimizda", state="*")
async def about_us(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "👨‍⚕️ Bizning klinika zamonaviy uskunalar va tajribali mutaxassislar bilan sizga xizmat qiladi.\n"
        "Batafsil: https://google.uz"
    )
