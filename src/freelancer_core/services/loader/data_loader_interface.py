from abc import ABC, abstractmethod


class DataLoaderServiceInterface(ABC):
    @abstractmethod
    async def load(self, csv_path: str, table_name: str, chunksize: int = 10000):
        pass
