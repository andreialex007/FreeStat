import asyncio
from punq import Container
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.freelancer_core.services.ai.llm.llm_interface import LLMInterface
from src.freelancer_core.services.ai.llm.llm_service import LLMService
from src.freelancer_core.services.ai.questions.llm_question_interface import LLMQuestionServiceInterface
from src.freelancer_core.services.ai.questions.llm_question_service import LLMQuestionService
from src.freelancer_core.services.freelance_stat_service import FreelanceStatService
from src.freelancer_core.services.loader.data_loader_interface import DataLoaderServiceInterface
from src.freelancer_core.services.loader.data_loader_service import DataLoaderService
from src.freelancer_core.services.table.table_interface import TableServiceInterface
from src.freelancer_core.services.table.table_service import TableService

DB_URL = "sqlite+aiosqlite:///freelancer.sqlite"
TABLE_NAME = "freelancers"
CSV_PATH = "dataset.csv"

PREDEFINED_QUESTIONS = [
    "What is the average earnings per region?",
    "Which region has the most expert freelancers?",
    "How many freelancers completed more than 100 projects?",
]

async def init_db_and_load_if_needed(data_loader: DataLoaderServiceInterface, table_service: TableServiceInterface):
    try:
        schema = await table_service.get_table_schema(TABLE_NAME)
        print("Database already contains data.")
    except Exception:
        print("Please wait, loading data...")
        await data_loader.load(CSV_PATH, TABLE_NAME)
        print("✅ Data loaded successfully.")

async def main():
    # Dependency setup
    engine = create_async_engine(DB_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    container = Container()
    container.register(LLMInterface, LLMService).with_arguments(llm=ChatOpenAI(model="gpt-4", temperature=0))
    container.register(TableServiceInterface, TableService).with_arguments(session=async_session())
    container.register(LLMQuestionServiceInterface, LLMQuestionService).with_arguments(llm=container.resolve(LLMInterface))
    container.register(DataLoaderServiceInterface, DataLoaderService).with_arguments(table_service=container.resolve(TableServiceInterface))
    container.register(FreelanceStatService, FreelanceStatService).with_arguments(
        llm_question_service=container.resolve(LLMQuestionServiceInterface),
        table_service=container.resolve(TableServiceInterface),
        table_name=TABLE_NAME
    )

    # Init DB
    await init_db_and_load_if_needed(
        data_loader=container.resolve(DataLoaderServiceInterface),
        table_service=container.resolve(TableServiceInterface),
    )

    # Prompt for question
    print("\nSelect a question:")
    for idx, q in enumerate(PREDEFINED_QUESTIONS, 1):
        print(f"{idx}. {q}")
    selected = int(input("Enter the number of the question: ")) - 1
    question = PREDEFINED_QUESTIONS[selected]

    # Run query
    stat_service = container.resolve(FreelanceStatService)
    result = await stat_service.ask_and_query(question)

    print("\n📊 Result:")
    for row in result:
        print(row)

if __name__ == "__main__":
    asyncio.run(main())
