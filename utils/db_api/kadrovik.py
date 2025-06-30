from utils.db_api.main_db import Database


class KadrovikDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_employee(self, user_id, vacancy, fullname, birthdate, phone, education, specialty, region, district):
        sql = """ INSERT INTO employee (user_id, vacancy, fullname, birthdate, phone, education, specialty, region, district) 
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) """
        return await self.db.execute(sql, user_id, vacancy, fullname, birthdate, phone, education, specialty, region,
                                     district, execute=True)

    async def delete_employee_by_telegram_id(self, telegram_id: str):
        sql = """
        DELETE FROM employee
        WHERE user_id = (SELECT id FROM users WHERE telegram_id = $1)
        """
        await self.db.execute(sql, telegram_id, execute=True)
