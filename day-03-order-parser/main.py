from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior

agent = Agent(
        
        "groq:llama-3.3-70b-versatile",
        instructions=(
                    "You are  a specialist doctor in general medicine who knows how to write health related reports"
            )
        )

history = None 

while True:

    prompt = input("Enter prompt> ")
    if prompt.lower() in {"quit", "exit"}:
        break
    if not prompt:
        continue
    try:
        result = agent.run_sync(prompt, message_history=history)
        print(result.output)
        history = result.all_messages()

    except httpx.HTTPError as e:
        print("couldn't reach the service")
    except Exception as e:
        print(f"unexpected: {type(e).__name__}: {e}")

