from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from src.freelancer_core.llm_interface import LLMInterface

class LLMService(LLMInterface):
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    async def ask(self, prompt: str) -> str:
        messages = [HumanMessage(content=prompt)]
        response = await self.llm.ainvoke(messages)
        return response.content.strip()
