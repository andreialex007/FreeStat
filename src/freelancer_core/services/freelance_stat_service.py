from typing import Any

from src.freelancer_core.services.ai.questions.llm_question_interface import LLMQuestionServiceInterface
from src.freelancer_core.services.freelance_stat_interface import FreelanceStatServiceInterface
from src.freelancer_core.services.table.table_interface import TableServiceInterface


class FreelanceStatService(FreelanceStatServiceInterface):
    def __init__(
        self,
        llm_question_service: LLMQuestionServiceInterface,
        table_service: TableServiceInterface,
        table_name: str
    ):
        self.llm_question_service = llm_question_service
        self.table_service = table_service
        self.table_name = table_name

    async def ask_and_query(self, question: str) -> list[tuple[Any]]:
        schema = await self.table_service.get_table_schema(self.table_name)
        sql = await self.llm_question_service.ask_sql_question(question, schema, self.table_name)
        return await self.table_service.execute_raw_sql(sql)
