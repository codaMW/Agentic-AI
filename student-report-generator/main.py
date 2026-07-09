from pydantic_ai import Agent
from pydantic import BaseModel

class StudentReport(BaseModel):

    name: str
    subject: str
    grade: int
    strength: list[str]
    improvements: list[str]

agent = Agent(
        "groq:qwen/qwen3-32b",
        instructions=(

            """ 
                You are an experienced school principal.
                Generate concise, professional student reports.
                Always fill every field in the StudentReport schema.
                Keep strengths and improvements realistic and actionable.
                Never return text outside the schema.
            """
            ),
        output_type=StudentReport
        )

history = None

while True:

    prompt = input("\nyou> ")

    if prompt.lower() in {"exit", "quit"}:
        break
    if not prompt:
        continue

    try:
        result = agent.run_sync(prompt, message_history=history)
        report = result.output
        print(f"""
        name: {report.name}
        subject: {report.subject}
        grade: {report.grade}
        strength: {report.strength}
        improvements: {report.improvements}
        """
        )

        history = result.all_messages()

    except Exception as e:
        print(f"Error: {type(e).__name__} {e}")
