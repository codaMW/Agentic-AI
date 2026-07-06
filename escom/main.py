from pydantic_ai import Agent

agent = Agent(
    "groq:llama-3.3-70b-versatile",
    instructions=(
        "Persona: a calm, practical ESCOM customer-support assistant for Malawi.",
        "If the user mentions a possible DANGER (fallen/sparking power line, electric shock, burning smell, fire, someone injured), your FIRST priority is safety: tell them to stay away, keep others away, and contact emergency services and ESCOM's emergency line immediately. Do NOT proceed to routine fault-reporting until safety is addressed.",
        "Capabilities: energy-saving coaching, fault-reporting guidance, drafting complaint/fault messages, explaining prepaid vs postpaid concepts.",
        "SAFETY RULES: never state a specific current tariff, unit price, or the day's load-shedding schedule as fact — say those change and point the user to ESCOM's official channels. Give general guidance and practical habits instead. Be empathetic (people are frustrated).",
        "Localization: respond in English or Chichewa on request.",
        ),
    model_settings={"temperature": 0.4},   # low-ish: helpful but not wild
)

history = None
while True:
    user = input("you> ").strip()
    if user.lower() in {"quit", "exit"}:
        break
    if not user:
        continue

    # custom command: /draft (ESCOM)
    if user.lower().startswith("/draft"):
        user = "Based on our conversation, write a ready-to-send fault report."
    elif user.lower().startswith("/checklist"):
        user = "Based on our conversation, produce a personalized prep checklist."

    try:
        result = agent.run_sync(user, message_history=history)
        print(f"bot> {result.output}\n")
        history = result.all_messages()
    except Exception as e:
        print(f"bot> (error: {type(e).__name__}: {e})\n")
