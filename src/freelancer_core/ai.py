import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)


async def ask_ai(question: str, schema: str, table_name: str) -> str:
    system_prompt = (
        f"You are a data analyst working with a PostgreSQL table named `{table_name}`.\n"
        f"Here is the schema:\n{schema}\n"
        "Your task is to write an accurate SQL query (PostgreSQL-compatible) to answer the user's question. "
        "Respond only with SQL code, no explanations, no formatting."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    response = await llm.ainvoke(messages)
    return response.content.strip()
