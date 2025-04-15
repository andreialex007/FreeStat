from src.freelancer_core.services.ai.llm.llm_interface import LLMInterface
from src.freelancer_core.services.ai.questions.llm_question_interface import LLMQuestionServiceInterface


class LLMQuestionService(LLMQuestionServiceInterface):
    def __init__(self, llm: LLMInterface):
        self.llm = llm

    async def ask_sql_question(self, question: str, schema: str, table_name: str) -> str:
        prompt = (
            f"You are a data analyst working with a SQLite table named `{table_name}`.\n"
            f"The table has the following schema:\n{schema}\n"
            f"Your task is to write a valid SQL query that answers the user's question:\n"
            f"{question}\n"
            f"Respond with ONLY the raw SQL query. Do NOT use Markdown, backticks, or explanations."
        )

        return await self.llm.ask(prompt)
