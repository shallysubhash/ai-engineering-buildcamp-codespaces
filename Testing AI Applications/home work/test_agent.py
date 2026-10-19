from sql_agent import agent
from sql_tools import con, setup_database


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