from pydantic_ai.messages import ModelResponse, ToolCallPart


def collect_tools(messages):
    """Extract database tool names in the order they were called."""
    return [
        part.tool_name
        for message in messages
        if isinstance(message, ModelResponse)
        for part in message.parts
        if isinstance(part, ToolCallPart)
        and part.tool_name in {"get_schema", "run_sql"}
    ]