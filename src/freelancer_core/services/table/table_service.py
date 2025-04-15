import asyncio
from typing import Any
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import inspect

from src.freelancer_core.services.table.table_interface import TableServiceInterface


class TableService(TableServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_insert(self, df: pd.DataFrame, table_name: str):
        records = df.to_dict(orient="records")
        stmt = insert(text(table_name)).values(records)

        async with self.session.begin():
            await self.session.execute(stmt)

    async def execute_raw_sql(self, sql: str) -> list[tuple[Any]]:
        async with self.session.begin():
            result = await self.session.execute(text(sql))
            return result.fetchall()

    async def get_table_schema(self, table_name: str) -> str:
        async with self.session.begin():
            inspector = inspect(self.session)
            columns = await asyncio.to_thread(inspector.get_columns, table_name)
            return "\n".join(f"{col['name']} ({col['type']})" for col in columns)
