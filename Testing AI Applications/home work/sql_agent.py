from pydantic import BaseModel, Field
from pydantic_ai import Agent

from sql_tools import SQLTools, setup_database


class SQLResult(BaseModel):
    sql_query: str
    result_text: str
    row_count: int = Field(
        ge=0,
        description="Number of result rows returned, excluding headers."
    )


sql_tools = SQLTools()

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=SQLResult,
    tools=[sql_tools.get_schema, sql_tools.run_sql],
    instructions=(
        "You answer questions using the DuckDB trips table. "
        "Always call get_schema first, before running any SQL. "
        "Use SELECT queries only. "
        "Run the query using run_sql before answering. "
        "Use only the actual tool results; never invent values. "
        "Trip distance is measured in miles. "
        "Return the executed SQL, its result as text, and the number "
        "of returned result rows. An AVG query returns one result row."
    ),
)


if __name__ == "__main__":
    setup_database()

    question = "What's the average trip distance for rides with 2 passengers?"
    result = agent.run_sync(question)

    print(result.output.model_dump_json(indent=2))