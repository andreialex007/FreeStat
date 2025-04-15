import pytest
from unittest.mock import AsyncMock
from langchain_core.language_models import BaseChatModel
from src.freelancer_core.services.ai.llm.llm_service import LLMService


@pytest.mark.asyncio
async def test_llm_service_ask():
    mock_llm = AsyncMock(spec=BaseChatModel)
    mock_llm.ainvoke.return_value.content = "SELECT * FROM freelancers;"

    service = LLMService(llm=mock_llm)
    result = await service.ask("Give me a query")

    assert result.strip().rstrip(';') == "SELECT * FROM freelancers"
    mock_llm.ainvoke.assert_called_once()
