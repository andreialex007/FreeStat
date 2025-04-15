import pandas as pd

from src.freelancer_core.services.loader.data_loader_interface import DataLoaderServiceInterface
from src.freelancer_core.services.table.table_interface import TableServiceInterface


class DataLoaderService(DataLoaderServiceInterface):
    def __init__(self, table_service: TableServiceInterface):
        self.table_service = table_service

    async def load(self, csv_path: str, table_name: str, chunksize: int = 10000):
        for chunk in pd.read_csv(csv_path, chunksize=chunksize):
            await self.table_service.bulk_insert(chunk, table_name)
