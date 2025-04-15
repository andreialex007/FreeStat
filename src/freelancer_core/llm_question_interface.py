from abc import ABC, abstractmethod

class LLMQuestionServiceInterface(ABC):
    @abstractmethod
    async def ask_sql_question(self, question: str, schema: str, table_name: str) -> str:
        pass
