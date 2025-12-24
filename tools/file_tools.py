# tools/file_tools.py

from utils.github_client import get_repo
from storage.file_cache import get_file_cached, set_file_cached
from config.settings import MAX_FILE_SIZE_KB


def get_file_content(path: str) -> str:
    cached = get_file_cached(path)
    if cached:
        return cached

    repo = get_repo()
    file = repo.get_contents(path)

    size_kb = file.size / 1024
    if size_kb > MAX_FILE_SIZE_KB:
        raise ValueError(f"File too large: {size_kb:.2f} KB")

    content = file.decoded_content.decode()
    set_file_cached(path, content)
    return content
