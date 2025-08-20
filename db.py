import asyncpg
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

async def init_db():
    conn = await asyncpg.connect(**DB_CONFIG)
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        title TEXT,
        start_ts TIMESTAMP NOT NULL,
        end_ts TIMESTAMP
    );
    """)
    await conn.close()

async def insert_event(user_id: int, title: str, start_ts: str, end_ts: Optional[str]):
    conn = await asyncpg.connect(**DB_CONFIG)
    await conn.execute("""
    INSERT INTO events (user_id, title, start_ts, end_ts)
    VALUES ($1, $2, $3, $4)
    """, user_id, title, start_ts, end_ts)
    await conn.close()
