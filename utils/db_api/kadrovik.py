from utils.db_api.main_db import Database


class KadrovikDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_employee(self, vacancy, fullname, birthdate, phone, education, specialty, region, district):
        sql = """ INSERT INTO employee (vacancy, fullname, birthdate, phone, education, specialty, region, district) 
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id """
        return await self.db.execute(sql, vacancy, fullname, birthdate, phone, education, specialty, region, district,
                                     fetchval=True)

    async def delete_book(self, book_id):
        await self.db.execute("DELETE FROM books WHERE book_id = $1", book_id, execute=True)

    async def delete_book_by_row_id(self, row_id):
        await self.db.execute("DELETE FROM books WHERE id = $1", row_id, execute=True)

    async def delete_book_not_book_id(self):
        await self.db.execute(""" DELETE FROM books WHERE book_id IS NULL """, execute=True)
