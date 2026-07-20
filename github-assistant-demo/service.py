from models import Repository


class GitHubService:

    def __init__(self):

        self.repositories = [
                Repository(
                name="rust-for-bitcoiners",
                description="My journey learning rust",
                language="Rust",
                stars= 8,
                owner="codaMW",
                ),

                Repository(
                name="Mostro",
                description=
                    """
                    Return all repositories owned by the user."
                    Use this tool whenever the user asks to list, display,or show their repositories.
                    """,
                language="Rust",
                stars= 50,
                owner="ngruch",
                ),

                Repository(
                name="rust-payjoin",
                description=
                """
                The main Payjoin Dev Kit library which provides tools for implementing both Async and Simple Payjoin. payjoin implements Payjoin session persistence support and IO utilities for interacting with OHTTP relays in Async Payjoin integrations.
                """,
                language="Rust",
                stars=100,
                owner="Dan",
                ),

                Repository(
                name="agent-ai",
                description="My journey learning agentic ai",
                language="Python",
                stars=25,
                owner="codaMW",
                ),

                Repository(
                name="backend-engineering",
                description="my journey learning backend engineering",
                language="Rust",
                stars= 1,
                owner="codaMW",
                ),
                ]

    def get_all_repositories(self) -> list[Repository]:

        return self.repositories

    def get_repo_owners(self) -> list[str]:
        owners = set(repo.owner for repo in self.repositories)
        return list(owners)

        


