from src.freelancer_core.llm_interface import LLMInterface
from src.freelancer_core.llm_question_interface import LLMQuestionServiceInterface

class LLMQuestionService(LLMQuestionServiceInterface):
    def __init__(self, llm: LLMInterface):
        self.llm = llm

    async def ask_sql_question(self, question: str, schema: str, table_name: str) -> str:
        prompt = (
            f"You are a data analyst working with a PostgreSQL table named `{table_name}`.\n"
            f"Here is the schema:\n{schema}\n"
            f"Write a valid SQL query (PostgreSQL syntax) that answers this question:\n"
            f"{question}\n"
            f"Respond only with raw SQL code, no explanations, markdown, or formatting."
        )

        return await self.llm.ask(prompt)
