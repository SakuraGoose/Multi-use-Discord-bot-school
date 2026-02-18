import aiomysql

async def init_db(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                balance BIGINT NOT NULL DEFAULT 0
            )
            """)
            await conn.commit()

class EconomyDB:
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
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE users SET balance = balance + %s WHERE user_id = %s",
                    (amount, user_id)
                )
                await conn.commit()

    async def set_balance(self, user_id: int, amount: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO users (user_id, balance) VALUES (%s, %s) "
                    "ON DUPLICATE KEY UPDATE balance = %s",
                    (user_id, amount, amount)
                )
                await conn.commit()