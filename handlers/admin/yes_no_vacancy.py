from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from magic_filter import F

from keyboards.inline.admin_ikb import admin_check_ikb
from loader import dp, bot, kdb
from states.admin import AdminStates


@dp.callback_query_handler(F.data.startswith("admin_yes:"), state="*")
async def handle_vacancy_yes(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.data.split(":")[1]
    await bot.send_message(
        chat_id=user_id,
        text="Arizangiz qabul qilindi! Ma'lumotlaringiz ko'rib chiqilgach, ma'qul ko'rilsangiz Sizga aloqaga chiqamiz!"
    )
    await call.message.edit_text(
        text="Ma'lumotlar qabul qilindi va bu haqidagi xabar ariza yuboruvchiga ham jo'natildi!"
    )


@dp.callback_query_handler(F.data.startswith("admin_no:"), state="*")
async def handle_vacancy_no(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(
        user_id=call.data.split(":")[1]
    )
    await call.message.edit_text(
        text="Rad etilish sababini kiriting:"
    )
    await AdminStates.NO_TEXT.set()


@dp.message_handler(state=AdminStates.NO_TEXT, content_types=types.ContentType.TEXT)
async def handle_no_text(message: types.Message, state: FSMContext):
    await state.update_data(no_text=message.text)
    user_id = (await state.get_data()).get("user_id")
    await message.answer(
        text="Xabaringiz qabul qilindi! Tasdiqlaysizmi?", reply_markup=admin_check_ikb(user_id=user_id)
    )
    await AdminStates.CHECK_NO_TEXT.set()


@dp.callback_query_handler(state=AdminStates.CHECK_NO_TEXT)
async def handle_check_no(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    await kdb.delete_employee_by_telegram_id(telegram_id=user_id)

    if call.data.startswith("reenter:"):
        await handle_vacancy_no(call=call, state=state)

    elif call.data.startswith("admincheck:"):
        data = await state.get_data()
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"Arizangiz rad etildi!\n\nSabab:\n{data['no_text']}"
            )
        except BotBlocked:
            await call.message.edit_text(
                text="Xabar foydalanuvchiga yuborilmadi! Foydalanuvchi botni block qilgan!"
            )
            return
        except ChatNotFound:
            await call.message.edit_text(
                text="Xabar foydalanuvchiga yuborilmadi! Foydalanuvchi topilmadi!"
            )
            return
        else:
            await call.message.edit_text(
                text="Xabar foydalanuvchiga yuborildi!"
            )
        await state.finish()
