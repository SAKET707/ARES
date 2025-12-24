# utils/github_client.py

from github import Github
from config.settings import GITHUB_TOKEN

# These will be set once per session
_github_client = None
_repo = None


def init_repo(owner: str, repo_name: str):
    """
    Initialize GitHub client and repository.
    Must be called ONCE when user selects a repo.
    """
    global _github_client, _repo

    _github_client = Github(GITHUB_TOKEN)
    _repo = _github_client.get_repo(f"{owner}/{repo_name}")


def get_repo():
    """
    Return initialized repository object.
    """
    if _repo is None:
        raise RuntimeError("Repository not initialized. Call init_repo() first.")
    return _repo
