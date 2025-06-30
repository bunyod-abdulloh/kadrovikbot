from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_get_keys_ikb():
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton(text="Excel kiritish", callback_data=f"admin_keys_xls"))
    btn.add(InlineKeyboardButton(text="Matn kiritish", callback_data=f"admin_keys_text"))
    return btn


def admin_check_ikb(user_id):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.row(InlineKeyboardButton(text="♻️ Qayta kiritish", callback_data=f"reenter:{user_id}"),
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"admin:yes_{user_id}"))
    return btn


def yes_no_ikb(user_id):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(InlineKeyboardButton(text="❌ Yo'q", callback_data=f"admin_no:{user_id}"),
            InlineKeyboardButton(text="✅ Ha", callback_data=f"admin_yes:{user_id}"))
    return btn


def rename_books_ikb(books):
    btn = InlineKeyboardMarkup(row_width=1)
    for book in books:
        btn.insert(InlineKeyboardButton(text=book['name'], callback_data=f"rename_books:{book['book_id']}"))
    return btn
