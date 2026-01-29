import aiosqlite
from abc import ABC, abstractmethod

DB_PATH = "economy.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            guild_id INTEGER PRIMARY KEY,
            balance INTEGER NOT NULL DEFAULT 0,
            bank INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, guild_id)
        )
        """)
        await db.commit()

class EconomyRepo(ABC):
    @abstractmethod
    async def ensure_user(self, user_id: int, guild_id: int):
        ...
    
    @abstractmethod
    async def get_balance(self, user_id: int, guild_id: int) -> int:
        ...

    @abstractmethod
    async def add_balance(self, user_id: int, guild_id: int, amount: int):
        ...

    @abstractmethod
    async def get_bank(self, user_id: int, guild_id: int) -> int:
        ...

    @abstractmethod
    async def add_bank(self, user_id: int, guild_id: int, amount: int):
        ...


    
class SQLiteEco(EconomyRepo):
    def __init__(self, db_path = "economy.db"):
        self.db_path = db_path    

    async def ensure_user(self, user_id: int, guild_id: int):
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                    (user_id),
                )
                await db.commit()

    async def get_balance(self, user_id: int, guild_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT balance FROM users WHERE user_id = ?",
                (user_id,)
            ) as cur:
                row = await cur.fetchone()
                return row[0] if row else 0
            
    async def add_balance(self, user_id: int, guild_id: int, amount: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()

    async def get_bank(self, user_id: int, guild_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELCET bank FROM users WHERE user_id = ?",
                (user_id),
            ) as cur:
                row = await cur.fetchone()
                return row[0] if row else 0
            
    async def add_bank(self, user_id: int, guild_id: int, amount: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET bank = bank + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()