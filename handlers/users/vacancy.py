import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.default.users_dkb import vacancy_menu, phone_cb, user_yes_no, main_menu_cb
from keyboards.inline.admin_ikb import yes_no_ikb
from loader import dp, kdb, udb
from states.users import AnketaStates


@dp.message_handler(F.text == "💼 Bo'sh ish o‘rinlari", state="*")
async def vacancies(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "📢 Hozirda quyidagi bo‘sh ish o‘rinlari mavjud:\n"
        "• Stomatolog\n• Qabul admini\n• Laborant",
        reply_markup=vacancy_menu
    )


@dp.message_handler(F.text.in_({"🦷 Stomatolog", "👩‍💼 Qabul admini", "🧪 Laborant"}), state="*")
async def start_job_application(message: types.Message, state: FSMContext):
    vacancy = message.text.split(" ", 1)[1]
    await state.update_data(vacancy=vacancy)
    await message.answer("📝 Iltimos, ism familiyangizni kiriting:\n\nMasalan: *Islomov Anvar*", parse_mode="Markdown")
    await AnketaStates.FULLNAME.set()


@dp.message_handler(state=AnketaStates.FULLNAME)
async def get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("🎂 Tug‘ilgan sanangizni kiriting:\n\nMasalan: *1998-04-12*", parse_mode="Markdown")
    await AnketaStates.BIRTHDATE.set()


@dp.message_handler(state=AnketaStates.BIRTHDATE)
async def get_birthdate(message: types.Message, state: FSMContext):
    await state.update_data(birthdate=message.text)
    await message.answer("🎓 Ma'lumotingiz:\n\nMasalan: *Oliy, ToshPTI, 2020-yil*", parse_mode="Markdown")
    await AnketaStates.EDUCATION.set()


@dp.message_handler(state=AnketaStates.EDUCATION)
async def get_education(message: types.Message, state: FSMContext):
    await state.update_data(education=message.text)
    await message.answer("🔧 Mutaxassisligingiz:\n\nMasalan: *Tish shifokori*", parse_mode="Markdown")
    await AnketaStates.SPECIALTY.set()


@dp.message_handler(state=AnketaStates.SPECIALTY)
async def get_specialty(message: types.Message, state: FSMContext):
    await state.update_data(specialty=message.text)
    await message.answer("📍 Viloyatingiz:\n\nMasalan: *Farg‘ona*", parse_mode="Markdown")
    await AnketaStates.REGION.set()


@dp.message_handler(state=AnketaStates.REGION)
async def get_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    await message.answer("🏙 Tumaningiz:\n\nMasalan: *Qo‘qon shahri*", parse_mode="Markdown")
    await AnketaStates.DISTRICT.set()


@dp.message_handler(state=AnketaStates.DISTRICT)
async def finish_anketa(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer(
        "📱 Telefon raqamingizni yuboring:\n\nMasalan: *+998901234567*\n\nTelefon raqam yuborish tugmasini bosing.",
        reply_markup=phone_cb,
        parse_mode="Markdown"
    )
    await AnketaStates.PHONE.set()


@dp.message_handler(state=AnketaStates.PHONE, content_types=['contact', 'text'])
async def get_phone(message: types.Message, state: FSMContext):
    phone = None
    if message.content_type == 'contact':
        phone = message.contact.phone_number.strip()
    elif message.content_type == 'text':
        phone = message.text.strip()

    if phone:
        if phone.startswith("998") and len(phone) == 12:
            phone = "+" + phone

        if not re.fullmatch(r"\+998\d{9}", phone):
            return await message.answer(
                "❌ Telefon raqamingiz noto‘g‘ri formatda. Iltimos, +998 bilan boshlanuvchi 9 xonali raqam yuboring.")
    else:
        return await message.answer("❌ Telefon raqam topilmadi.")

    await state.update_data(phone=phone)

    data = await state.get_data()

    text = (
        f"📌 Lavozim: {data['vacancy']}\n"
        f"👤 F.I.Sh.: {data['fullname']}\n"
        f"🎂 Tug‘ilgan sana: {data['birthdate']}\n"
        f"📱 Telefon raqam: {phone}\n"
        f"🎓 Ma’lumoti: {data['education']}\n"
        f"🔧 Mutaxassisligi: {data['specialty']}\n"
        f"📍 Hudud: {data['region']}, {data['district']}"
    )

    await message.answer(f"Kiritgan ma'lumotlaringizni tekshirib chiqib kerakli tugmani bosing\n\n{text}",
                         reply_markup=user_yes_no)
    await AnketaStates.CHECK.set()
    return None


@dp.message_handler(state=AnketaStates.CHECK, content_types=types.ContentType.TEXT)
async def check_datas(message: types.Message, state: FSMContext):
    if message.text == "✅ Tasdiqlash":
        data = await state.get_data()

        text = (
            f"📥 *Yangi ariza qabul qilindi!*\n\n"
            f"📌 Lavozim: {data['vacancy']}\n"
            f"👤 F.I.Sh.: {data['fullname']}\n"
            f"🎂 Tug‘ilgan sana: {data['birthdate']}\n"
            f"📱 Telefon raqam: {data['phone']}\n"
            f"🎓 Ma’lumoti: {data['education']}\n"
            f"🔧 Mutaxassisligi: {data['specialty']}\n"
            f"📍 Hudud: {data['region']}, {data['district']}"
        )

        # UsersDB ga qo'shamiz
        user_id = await udb.add_user(telegram_id=message.from_user.id)

        # KadrovikDB ga vaqtincha joylab turamiz
        await kdb.add_employee(
            user_id=user_id, vacancy=data['vacancy'], fullname=data['fullname'], birthdate=data['birthdate'],
            phone=data['phone'], education=data['education'], specialty=data['specialty'], region=data['region'],
            district=data['district']
        )

        for admin_id in ADMINS:
            try:
                await message.bot.send_message(chat_id=admin_id, text=text, parse_mode="Markdown",
                                               reply_markup=yes_no_ikb(
                                                   user_id=message.from_user.id
                                               ))
            except Exception as err:
                print(f"Adminga yuborishda xatolik: {err}")

        await message.answer("✅ Rezyumengiz qabul qilindi! Tez orada Siz bilan bog‘lanamiz!",
                             reply_markup=main_menu_cb)

    elif message.text == "♻️ Qayta kiritish":
        await state.finish()
        await vacancies(message=message, state=state)
