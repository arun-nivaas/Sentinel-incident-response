import os
from github import Github, GithubException
from typing import Any, Dict

class GitHubClientError(Exception):
    pass

class GitHubClient:

    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        owner = os.getenv("GITHUB_REPO_OWNER")
        repo_name = os.getenv("GITHUB_REPO_NAME")

        if not all([token, owner, repo_name]):
            raise GitHubClientError("Missing GitHub configuration in .env")
        
        self.client = Github(token)
        self.repo = self.client.get_repo(f"{owner}/{repo_name}")

    def create_issue(self, title: str, body: str, labels: list[str] | None = None) -> Dict[str, Any]:
        try:
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels or [],
            )
            return {"issue_url": issue.html_url, "issue_number": issue.number}
        except GithubException as e:
            raise GitHubClientError(f"Failed to create GitHub issue: {e}") from e