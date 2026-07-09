from pydantic_ai import Agent
from pydantic import BaseModel

class MovieRecommendation(BaseModel):

    title: str
    genre: str
    reason: str

agent = Agent(
        "groq:llama-3.3-70b-versatile",
        instructions="""
        You are a movie recommendation assistant.
        Always recommend exactly one movie.
        Always produce a valid MovieRecommendation object.
        Never explain outside the schema.
        """,
        output_type=MovieRecommendation,
        )

history = None

while True:
    prompt = input("\nyou> ")

    if prompt.lower() in { "exit", "quit" }:
        break
    if not prompt:
        continue
    try:
        result = agent.run_sync(prompt, message_history=history)
        movie = result.output
        print(f"""
        Title : {movie.title}
        Genre : {movie.genre}
        Reason: {movie.reason}
              """)
        history = result.all_messages()
    except Exception as e:
        print(f"Error {type(e).__name__} {e}")

        
