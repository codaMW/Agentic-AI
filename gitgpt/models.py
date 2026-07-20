from pydantic import BaseModel


class GitHubInfo(BaseModel):

    html_url: str | None
    user_view_type: str | None
    name: str | None
    company: str | None
    email: str | None
    bio: str | None
    public_repos: int | None
    created_at: str | None


class RepoInfo(BaseModel):

    full_name: str | None
    private: bool | None
    description: str | None
    fork: bool | None
    forks_count: int | None
    language: str | None
    has_issues: bool | None
    open_issues_count: int | None




