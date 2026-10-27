from pydantic_ai import Agent
from trivia_tools import TriviaTools
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()

instructions = """You are a trivia quizmaster. When asked to play trivia:
1. Use the available tools to fetch trivia questions.
2. Ask the player one question at a time with multiple-choice options.
3. Wait for their answer before moving to the next question.
4. Explain why the correct answer is correct, with interesting context.
5. Give the final score after all questions.
"""

trivia_tools = TriviaTools()

agent = Agent(
    "openai:gpt-4o-mini",
    name="agent",
    tools=[trivia_tools.get_categories, trivia_tools.get_questions],
    instructions=instructions,
)

def run(prompt):
    message_history = []

    while True:
        result = agent.run_sync(prompt, message_history=message_history)
        print(result.output)
        message_history = result.all_messages()

        prompt = input("You (write 'stop' to stop): ")
        if not prompt or prompt.lower().strip() == "stop":
            break


with logfire.span("trivia_session"):
    run("Let's play 5 easy questions from Science & Nature")