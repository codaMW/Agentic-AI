#Author: Yankho Ngolleka - codaMW

# Borrow the Agent "blueprint" from the pydantic_ai library.
from pydantic_ai import Agent

# Hire an assistant. First argument = which brain (provider:model).
agent = Agent(
    'groq:llama-3.3-70b-versatile',
    # The agent's standing orders — its personality and rules.
    instructions='You are a helpful assistant. Answer clearly and concisely.',
)

# Give it a task and wait right here for the answer.
result = agent.run_sync('What is the capital of Malawi, and one fun fact about it?')

# The final text answer lives in .output — show it on screen.
print(result.output)
