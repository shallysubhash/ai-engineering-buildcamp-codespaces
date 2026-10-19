from sql_agent import agent
from sql_tools import con, setup_database
from utils import collect_tools
from judge import evaluate_agent_performance, assert_criteria


def test_trips_with_more_than_five_passengers():
    setup_database()

    expected_count = con.execute(
        "SELECT COUNT(*) FROM trips WHERE passenger_count > 5"
    ).fetchone()[0]

    result = agent.run_sync(
        "How many trips had more than 5 passengers? "
        "Return the exact count as digits without thousands separators."
    )
    output = result.output

    assert isinstance(output.sql_query, str)
    assert output.sql_query.strip()
    assert str(expected_count) in output.result_text





def test_schema_before_sql():
    setup_database()

    result = agent.run_sync("What is the most common payment type?")
    tool_calls = collect_tools(result.all_messages())

    assert tool_calls, "The agent did not call any database tools"
    assert tool_calls[0] == "get_schema"
    assert "run_sql" in tool_calls

    print(f"Tool calls: {tool_calls}")  





def test_highest_average_fare_hour():
    setup_database()

    question = (
        "Which hour of the day has the highest average fare amount? "
        "Include the hour and the actual average fare amount in your answer."
    )

    reference_rows = con.execute("""
        SELECT
            EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
            AVG(fare_amount) AS average_fare
        FROM trips
        GROUP BY pickup_hour
        ORDER BY average_fare DESC
        LIMIT 1
    """).fetchall()

    hour, average_fare = reference_rows[0]
    reference = (
        f"Pickup hour: {hour} (0–23); "
        f"average fare amount: ${average_fare:.6f}"
    )

    result = agent.run_sync(question)

    criteria = [
        "The SQL query correctly calculates average fare by hour of day.",
        "The result identifies a specific hour as having the highest average fare.",
        "The result includes the actual average fare amount.",
    ]

    evaluation = evaluate_agent_performance(
        question=question,
        output=result.output,
        criteria=criteria,
        reference=reference,
    )

    print(f"\nDatabase answer: {reference}")
    print(result.output.model_dump_json(indent=2))
    print(evaluation.model_dump_json(indent=2))

    assert_criteria(evaluation, criteria)   