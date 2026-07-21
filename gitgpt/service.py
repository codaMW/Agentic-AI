from models import GitHubInfo, RepoInfo, RepoContent
import httpx
import base64

class GitHubService:

    def get_user_info(self, name: str) -> GitHubInfo:
        BASE_URL = "https://api.github.com"
        url = f"{BASE_URL}/users/{name}"
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return GitHubInfo (
                 html_url=data["html_url"],
                 user_view_type=data["user_view_type"],
                 name=data["name"],
                 company=data["company"],
                 email=data["email"],
                 bio=data["bio"],
                 public_repos=data["public_repos"],
                 created_at=data["created_at"],

                )


    def get_repo_information(self, name: str, repo: str) -> RepoInfo:
        BASE_URL = "https://api.github.com"
        url = f"{BASE_URL}/repos/{name}/{repo}"
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return RepoInfo (
                 full_name=data["full_name"],
                 private=data["private"],
                 description=data["description"],
                 fork=data["fork"],
                 forks_count=data["forks_count"],
                 language=data["language"],
                 has_issues=data["has_issues"],
                 open_issues_count=data["open_issues_count"],
                )



    def get_repo_content(self, name: str, repo: str) -> RepoContent:
        BASE_URL = "https://api.github.com"
        url = f"{BASE_URL}/repos/{name}/{repo}/contents/README.md"
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        content = base64.b64decode(data["content"])
        decoded_content = content.decode('utf-8')

        return RepoContent (
                sha=data["sha"],
                typ=data["type"],
                content=decoded_content[:10000]
                )

