import asyncio
import sqlite3
from typing import Any
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, MetaData, Table, Integer, Float, String, Column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import inspect
from sqlalchemy.sql.sqltypes import NullType

from src.freelancer_core.services.table.table_interface import TableServiceInterface


class TableService(TableServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_insert(self, df: pd.DataFrame, table_name: str):
        url = str(self.session.bind.url)
        if not url.startswith("sqlite"):
            raise RuntimeError("This bulk_insert is implemented only for SQLite.")

        db_path = url.split("///")[-1]

        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, index=False, if_exists="append")

    async def execute_raw_sql(self, sql: str) -> list[tuple[Any]]:
        async with self.session.begin():
            result = await self.session.execute(text(sql))
            return result.fetchall()

    async def get_table_schema(self, table_name: str) -> str:
        async with self.session.bind.connect() as conn:
            def _inspect(sync_conn):
                inspector = inspect(sync_conn)
                columns = inspector.get_columns(table_name)
                return ", ".join(f"{col['name']} {col['type']}" for col in columns)

            return await conn.run_sync(_inspect)
