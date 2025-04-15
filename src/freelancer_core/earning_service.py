from typing import Any
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert


class EarningService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def load(self, csv_path: str, table_name: str = "freelancers", chunksize: int = 10000):
        for chunk in pd.read_csv(csv_path, chunksize=chunksize):
            await self._bulk_insert(chunk, table_name)

    async def execute_raw_sql(self, sql: str) -> list[tuple[Any]]:
        async with self.session.begin():
            result = await self.session.execute(text(sql))
            return result.fetchall()

    async def _bulk_insert(self, df: pd.DataFrame, table_name: str):
        records = df.to_dict(orient="records")
        stmt = insert(text(table_name)).values(records)

        async with self.session.begin():
            await self.session.execute(stmt)
