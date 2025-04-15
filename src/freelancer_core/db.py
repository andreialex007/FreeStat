import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import inspect
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("POSTGRES_URL")
TABLE_NAME = os.getenv("TABLE_NAME", "freelancers")

engine: AsyncEngine = create_async_engine(DB_URL, echo=False)


async def get_engine() -> AsyncEngine:
    return engine


async def get_table_schema(engine: AsyncEngine, table_name: str) -> str:
    async with engine.begin() as conn:
        inspector = inspect(conn)
        columns = await asyncio.to_thread(inspector.get_columns, table_name)
        return "\n".join(f"{col['name']} ({col['type']})" for col in columns)
