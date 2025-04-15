from abc import ABC, abstractmethod
from typing import Any


class FreelanceStatServiceInterface(ABC):
    @abstractmethod
    async def ask_and_query(self, question: str, schema: str, table_name: str) -> list[tuple[Any]]:
        pass
