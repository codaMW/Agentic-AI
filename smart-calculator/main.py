from pydantic_ai import Agent
from pydantic_ai import RunContext

agent = Agent(
        "groq:llama-3.3-70b-versatile",
        instructions=("""
        You are a smart calculator with exception math skills and math error handling
        """)
        )

history = []

@agent.tool
def add(ctx: RunContext, a: int, b: int) -> int:

    """
    Add numbers

    Args:
        a: an integer
        b: an integer
    Return:
        The sum of the input numbers
    """
    return a + b


@agent.tool
def subtract(ctx: RunContext, a: int, b: int) -> int:

    """
    Subtract numbers

    Args:
        a: an integer
        b: an integer
    Return:
        The subtraction of the input numbers
    """

    return a - b


@agent.tool
def multiply(ctx: RunContext, a: int, b: int) -> int:

    """
    multiply numbers

    Args:
        a: an integer
        b: an integer
    Return:
        The product of the input numbers
    """

    return a * b



@agent.tool
def divide(ctx: RunContext, a: int, b: int) -> float:

    """
    Divide two numbers

    Args:
        a: Dividend
        b: Divisor
    Return:
        quotient
    Raises: 
        valueError: if b is equal to zero
    """
    if b == 0:
        raise ValueError("Division by zero is undefined")
    return a / b



while True:
    prompt = input("\nyou> ")

    if prompt.lower() in { "exit", "quit" }:
        break
    if not prompt:
        continue

    try:
        result = agent.run_sync(prompt, message_history=history)
        print(f"\nbot> {result.output}")
        history = result.all_messages()
    except Exception as e:
        print(f"Error {type(e).__name__} {e}")
