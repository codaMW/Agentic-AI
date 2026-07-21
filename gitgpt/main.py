from pydantic import BaseModel
from models import GitHubInfo, RepoInfo, RepoContent
from service import GitHubService
from pydantic_ai import Agent, RunContext


agent = Agent(
        "groq:llama-3.3-70b-versatile",

        instructions=(
            """
            You are a helpful GitHub profile assistant. Always summarize the tool data into a readable message.
            """
            ),

        deps_type=GitHubService
        )

@agent.tool
def user_info(ctx: RunContext[GitHubService], name: str) -> GitHubInfo:

    """
    Retrieve a GitHub user's public profile.

    Args:
        name: GitHub username.

    Returns:
        A GitHubInfo object containing profile metadata.
    """

    service = ctx.deps

    return service.get_user_info(name)



@agent.tool
def repo_information(ctx: RunContext[GitHubService], name: str, repo: str) -> RepoInfo:
    """
    Retrieve a GitHub repository information
    Args:
        name: Github username
        repo: Github repository name
    Returns:
    A RepoInfo object containing repository data.
    """
    serve = ctx.deps
    return serve.get_repo_information(name, repo)




@agent.tool
def repo_content(ctx: RunContext[GitHubService], name: str, repo: str) -> RepoContent:

    """
    Retrieve a Github repository README.md information
    Args:
        name: Github username
        repo: Github repository name
    Returns:
    A RepoContent object that summarizes the repository’s README.md information.

    """

    service = ctx.deps

    return service.get_repo_content(name, repo)




service = GitHubService()
history = None


while True:

    prompt = input("you> ")
    if prompt.lower() in {"exit", "quit"}:
        break
    if not prompt:
        continue

    try:
        result = agent.run_sync(prompt, deps = service, message_history=history)
        print(f"bot> {result.output}")
        history = result.all_messages()
    except Exception as e:
        print(f"{type(e).__name__} {e}")
