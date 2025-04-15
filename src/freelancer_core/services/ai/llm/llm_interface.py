from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    async def ask(self, question: str) -> str:
        pass
