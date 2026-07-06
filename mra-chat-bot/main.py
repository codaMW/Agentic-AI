from pydantic_ai import Agent

agent = Agent(
        "groq:llama-3.3-70b-versatile",
        instructions=(
                """
                Persona: a friendly tax-literacy coach for Malawian small businesses and informal traders. Reassuring, jargon-free, encouraging of compliance.
                Capabilities: explain tax concepts (TPIN, PAYE, VAT, turnover tax) simply; coach through what registration/filing involves; produce prep checklists; draft questions to ask MRA.
                SAFETY RULES: NEVER state specific rates, thresholds, penalties, or deadlines as current fact — these change; direct users to MRA's official info or a licensed tax advisor for exact numbers. Clearly say you provide general education, not professional tax advice.
                Localization: English or Chichewa.
                """
            ),
        model_settings={ "temperature":0.4 }
        )
history = None

while True:

    prompt = input("you> ")

    if prompt.lower() in { "exit", "quit" }:
        break
    if not prompt:
        continue

    if prompt.lower().startswith("/draft"):
        prompt = "Based on our conversation, write a ready-to-send fault report."
    elif prompt.lower().startswith("/checklist"):
        prompt = "Based on our conversation, produce a personalized prep checklist."

    try:
        result = agent.run_sync(prompt, message_history=history)
        print(f"bot>{result.output}\n")
        history = result.all_messages()
    except Exception as e:
        print(f"bot> (error: {type(e).__name__}: {e})\n")
