import pytest
from unittest.mock import AsyncMock
from src.freelancer_core.services.freelance_stat_service import FreelanceStatService

@pytest.mark.asyncio
async def test_freelance_stat_service_ask_and_query():
    mock_llm_question_service = AsyncMock()
    mock_table_service = AsyncMock()
    mock_table_name = "freelancers"

    mock_table_service.get_table_schema.return_value = "MockSchema"
    mock_llm_question_service.ask_sql_question.return_value = "SELECT * FROM freelancers"
    mock_table_service.execute_raw_sql.return_value = [("John", 5000), ("Jane", 6000)]

    service = FreelanceStatService(
        llm_question_service=mock_llm_question_service,
        table_service=mock_table_service,
        table_name=mock_table_name
    )

    result = await service.ask_and_query("Show earnings")
    assert result == [("John", 5000), ("Jane", 6000)]

    mock_table_service.get_table_schema.assert_awaited_once_with(mock_table_name)
    mock_llm_question_service.ask_sql_question.assert_awaited_once_with("Show earnings", "MockSchema", mock_table_name)
    mock_table_service.execute_raw_sql.assert_awaited_once_with("SELECT * FROM freelancers")
