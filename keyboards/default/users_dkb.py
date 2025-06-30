from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_cb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("ℹ️ Biz haqimizda"), KeyboardButton("📞 Aloqa")],
        [KeyboardButton("💼 Bo'sh ish o‘rinlari"), KeyboardButton("🌐 Tilni o‘zgartirish")]
    ],
    resize_keyboard=True
)

vacancy_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🦷 Stomatolog")],
        [KeyboardButton("👩‍💼 Qabul admini"), KeyboardButton("🧪 Laborant")],
        [KeyboardButton("⬅️ Ortga")]
    ],
    resize_keyboard=True
)

phone_cb = ReplyKeyboardMarkup(resize_keyboard=True)
phone_cb.row(KeyboardButton(text="📱 Telefon raqam yuborish", request_contact=True))

user_yes_no = ReplyKeyboardMarkup(resize_keyboard=True)
user_yes_no.row("♻️ Qayta kiritish", "✅ Tasdiqlash")
