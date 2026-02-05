import aiosqlite
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

DB_PATH = "economy.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER NOT NULL DEFAULT 0,
            bank INTEGER NOT NULL DEFAULT 0,
            last_daily TEXT NOT NULL,
            streak INTEGER DEFAULT 1
        )
        """)
        await db.commit()

class EconomyRepo(ABC):
    @abstractmethod
    async def ensure_user(self, user_id: int):
        ...
    
    @abstractmethod
    async def get_balance(self, user_id: int) -> int:
        ...

    @abstractmethod
    async def add_balance(self, user_id: int, amount: int):
        ...

    @abstractmethod
    async def get_bank(self, user_id: int) -> int:
        ...

    @abstractmethod
    async def add_bank(self, user_id: int, amount: int):
        ...

    @abstractmethod
    async def claim_daily(self, user_id: int):
        ...


    
class SQLiteEco(EconomyRepo):
    def __init__(self, db_path = "economy.db"):
        self.db_path = db_path    

    async def ensure_user(self, user_id: int):
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                    (user_id,)
                )
                await db.commit()

    async def get_balance(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT balance FROM users WHERE user_id = ?",
                (user_id,)
            ) as cur:
                row = await cur.fetchone()
                return row[0] if row else 0
            
    async def add_balance(self, user_id: int, amount: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()

    async def get_bank(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT bank FROM users WHERE user_id = ?",
                (user_id,)
            ) as cur:
                row = await cur.fetchone()
                return row[0] if row else 0
            
    async def add_bank(self, user_id: int, amount: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET bank = bank + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()

    async def claim_daily(self, user_id: int):
        def can_claim(last_claim_str):
            if not last_claim_str:
                return True, None
            
            last_claim = datetime.fromisoformat(last_claim_str)
            time_diff = datetime.now() - last_claim

            if time_diff < timedelta(hours=24):
                time_remaining = timedelta(hours=24) - time_diff
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int(time_remaining.total_seconds() % 3600)
                return False, f"You can't claim yet! \n Come back in **{hours}h** and **{minutes}**m!"
            
            return True, time_diff
        
        def calc_streak(time_diff, current):
            if time_diff is None:
                return 1
            if time_diff <= timedelta(hours=36):
                return current + 1
            else:
                return 1
            
        def calc_reward(streak):
            base_reward = 1000
            if streak < 30:
                return 1000 * 1.05511**(streak)
            if streak >= 30:
                return 5000

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT last_daily, streak FROM users WHERE user_id = ?",
                (user_id,)
            ) as cur:
                row = await cur.fetchone()

            if row and row[0]:
                last_daily_str = row[0]
                current_streak = row[1]
            else:
                last_daily_str = None
                current_streak = 0




class EconomyRepoFactory:
    @staticmethod
    def create() -> EconomyRepo:
        return SQLiteEco()