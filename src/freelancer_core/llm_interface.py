from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    async def ask_ai(self, question: str, schema: str, table_name: str) -> str:
        pass
