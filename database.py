import aiomysql
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

async def init_db(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SHOW TABLES LIKE 'users'")
            if await cur.fetchone() is None:
                await cur.execute("""
                CREATE TABLE users (
                    user_id BIGINT PRIMARY KEY,
                    balance BIGINT NOT NULL DEFAULT 0,
                    bank BIGINT NOT NULL DEFAULT 0,
                    last_daily TEXT,
                    streak INTEGER DEFAULT 1
                )
                """)
            await conn.commit()

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
    async def set_balance(self, user_id: int, amount: int):
        ...

    @abstractmethod
    async def claim_daily(self, user_id: int) -> dict:
        ...

class MySQLEco(EconomyRepo):
    def __init__(self, pool):
        self.pool = pool

    async def ensure_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT IGNORE INTO users (user_id) VALUES (%s)",
                    (user_id,)
                )
                await conn.commit()

    async def get_balance(self, user_id: int) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT balance FROM users WHERE user_id = %s",
                    (user_id,)
                )
                row = await cur.fetchone()
                return row[0] if row else 0

    async def add_balance(self, user_id: int, amount: int):
        await self.ensure_user(user_id)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE users SET balance = balance + %s WHERE user_id = %s",
                    (amount, user_id)
                )
                await conn.commit()

    async def get_bank(self, user_id: int) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT bank FROM users WHERE user_id = %s",
                    (user_id,)
                )
                row = await cur.fetchone()
                return row[0] if row else 0

    async def add_bank(self, user_id: int, amount: int):
        await self.ensure_user(user_id)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE users SET bank = bank + %s WHERE user_id = %s",
                    (amount, user_id)
                )
                await conn.commit()

    async def set_balance(self, user_id: int, amount: int):
        await self.ensure_user(user_id)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE users SET balance = %s WHERE user_id = %s",
                    (amount, user_id)
                )
                await conn.commit()

    async def claim_daily(self, user_id: int) -> dict:
        await self.ensure_user(user_id)
        
        def can_claim(last_claim_str):
            if not last_claim_str:
                return True, None
            
            last_claim = datetime.fromisoformat(last_claim_str)
            time_diff = datetime.now() - last_claim

            if time_diff < timedelta(hours=24):
                time_remaining = timedelta(hours=24) - time_diff
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                return False, f"You can't claim yet! \n Come back in **{hours}h** and **{minutes}m**!"
            
            return True, time_diff
        
        def calc_streak(time_diff, current):
            if time_diff is None:
                return 1
            if time_diff <= timedelta(hours=36):
                return current + 1
            else:
                return 1
            
        def calc_reward(streak):
            if streak < 30:
                return int(1000 * 1.05511**(streak))
            else:
                return 5000

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT last_daily, streak FROM users WHERE user_id = %s",
                    (user_id,)
                )
                row = await cur.fetchone()

                if row and row[0]:
                    last_daily_str = row[0]
                    current_streak = row[1]
                else:
                    last_daily_str = None
                    current_streak = 0

                can_claim_result, time_diff = can_claim(last_daily_str)
                
                if not can_claim_result:
                    return {"success": False, "message": time_diff}
                
                # Calculate new streak and reward
                new_streak = calc_streak(time_diff, current_streak)
                reward = calc_reward(new_streak)
                
                # Update database
                now = datetime.now().isoformat()
                await cur.execute(
                    "UPDATE users SET balance = balance + %s, last_daily = %s, streak = %s WHERE user_id = %s",
                    (reward, now, new_streak, user_id)
                )
                await conn.commit()
                
                return {"success": True, "reward": reward, "streak": new_streak}

class EconomyRepoFactory:
    @staticmethod
    def create(pool) -> EconomyRepo:
        return MySQLEco(pool)