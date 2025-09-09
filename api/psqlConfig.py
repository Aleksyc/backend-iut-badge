import dotenv
import os
import asyncpg

dotenv.load_dotenv()

async def create_pool():
    return await asyncpg.create_pool(
        dsn=os.getenv("DB_URL"),
        min_size=1,
        max_size=10,
    )