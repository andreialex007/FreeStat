from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


class TableServiceInterface(ABC):
    @abstractmethod
    async def bulk_insert(self, df: pd.DataFrame, table_name: str):
        pass

    @abstractmethod
    async def execute_raw_sql(self, sql: str) -> list[tuple[Any]]:
        pass

    @abstractmethod
    async def get_table_schema(self, table_name: str) -> str:
        pass
