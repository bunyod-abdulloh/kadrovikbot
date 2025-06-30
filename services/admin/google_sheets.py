import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API ga ulanish uchun scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# JSON fayl yo‘li va ulanish
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "services/kadrovikbot-a8f37abb16d2.json", scope
)
client = gspread.authorize(creds)

# Google Sheets fayl nomi (oldindan Drive’da yaratilgan bo‘lishi kerak)
spreadsheet = client.open("Kadrovik_Arizalar")
sheet = spreadsheet.sheet1  # 1-sahifa bilan ishlaymiz


def write_headers_if_needed():
    headers = [
        "Lavozim", "F.I.Sh.", "Tug‘ilgan sana", "Telefon",
        "Ma’lumoti", "Mutaxassisligi", "Hudud", "Tuman"
    ]
    first_row = sheet.row_values(1)
    # Agar birinchi qator toza bo‘sh bo‘lsa, sarlavhalarni yozamiz
    if not any(cell.strip() for cell in first_row):
        sheet.insert_row(headers, 1)


def append_application(data: dict):
    """
    Ariza ma'lumotlarini yangi qatorda Google Sheets'ga yozadi.
    """
    write_headers_if_needed()

    row = [
        data.get("vacancy", ""),
        data.get("fullname", ""),
        data.get("birthdate", ""),
        data.get("phone", ""),
        data.get("education", ""),
        data.get("specialty", ""),
        data.get("region", ""),
        data.get("district", "")
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")
