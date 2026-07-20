from pydantic_ai import Agent, RunContext
from service import GitHubService
from models import Repository
from pydantic import BaseModel

agent = Agent(
        "groq:llama-3.3-70b-versatile",
        instructions=(
            "You are a Github assistant",
            "When users ask to list repositories use the list_repository tool",
            "Never invent repository information",
            ),
        deps_type=GitHubService
        )


@agent.tool
def list_repositories(ctx: RunContext[GitHubService]) -> list[Repository]:

    """
    Return all repositories owned by the user.
    Use this tool whenever the user asks to list, display,
    or show their repositories.
    """

    service = ctx.deps

    return service.get_all_repositories()

#@agent.tool
#def list_owners(ctx: RunContext[GitHubService]) -> list[str]:
    #"""
    #Returns the names of all the github repository owners
    #Use this tool whenever the user ask to list, display or show names 
    #of the repository owners not in a specific format just get the names and list
    #them not in any order or format
    #"""
    #service = ctx.deps

    #return servics.get_repo_owners()


history = None
service = GitHubService()


while True:

    prompt = input("\nyou> ")
    if prompt.lower() in {"exit", "quit"}:
        break
    if not prompt:
        continue

    try:
        result = agent.run_sync(prompt, deps=service, message_history=history)
        print(f"\nbot> {result.output}")
        history = result.all_messages()

    except Exception as e:
        print(f"{type(e).__name__} {e}")

