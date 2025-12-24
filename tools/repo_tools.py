# tools/repo_tools.py

from utils.github_client import get_repo
from storage.session_cache import get_cached, set_cached
from config.settings import MAX_TREE_ENTRIES

def _clean_readme(readme: str) -> str:
    """
    Extracts a clean, high-level description from README.md
    while preserving paragraph structure.
    """
    lines = readme.splitlines()
    paragraphs = []
    current = []

    stop_keywords = {
        "demo",
        "screenshot",
        "walkthrough",
        "installation",
        "usage",
        "getting started",
        "license",
    }

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        # Stop at noisy sections
        if any(k in lower for k in stop_keywords):
            break

        # Skip markdown noise
        if stripped.startswith("![") or stripped.startswith("<img"):
            continue
        if stripped.startswith("---"):
            break

        # Paragraph handling
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue

        # Remove heading markers but keep text
        if stripped.startswith("#"):
            stripped = stripped.lstrip("#").strip()

        current.append(stripped)

        # Hard cap: ~3 paragraphs total
        if len(paragraphs) >= 3:
            break

    if current and len(paragraphs) < 3:
        paragraphs.append(" ".join(current))

    return "\n\n".join(paragraphs)


# ------------------------------------------------------------
# REPO TREE
# ------------------------------------------------------------

def get_repo_tree(path="", depth=0):
    # cache only at root
    if path == "":
        cached = get_cached("repo_tree")
        if cached:
            return cached

    repo = get_repo()
    contents = repo.get_contents(path)

    tree = []

    for idx, item in enumerate(contents):
        if idx >= MAX_TREE_ENTRIES:
            break

        node = {
            "name": item.name,
            "path": item.path,
            "type": item.type,
        }

        if item.type == "dir":
            node["children"] = get_repo_tree(item.path, depth + 1)
        else:
            node["children"] = None

        tree.append(node)

    if path == "":
        set_cached("repo_tree", tree)

    return tree

def format_repo_tree(tree, prefix=""):
    lines = []

    for idx, node in enumerate(tree):
        is_last = idx == len(tree) - 1
        connector = "└── " if is_last else "├── "

        if node["type"] == "dir":
            lines.append(f"{prefix}{connector}{node['name']}/")
            extension = "    " if is_last else "│   "
            lines.extend(
                format_repo_tree(
                    node["children"],
                    prefix + extension,
                )
            )
        else:
            lines.append(f"{prefix}{connector}{node['name']}")

    return lines



# ------------------------------------------------------------
# FILE PATH RESOLUTION
# ------------------------------------------------------------

def find_file_path(filename: str):
    repo = get_repo()
    matches = []

    def walk(path=""):
        contents = repo.get_contents(path)
        for item in contents:
            if item.type == "file" and item.name == filename:
                matches.append(item.path)
            elif item.type == "dir":
                walk(item.path)

    walk("")
    return matches


# ------------------------------------------------------------
# README / REQUIREMENTS
# ------------------------------------------------------------

def get_readme():
    cached = get_cached("readme")
    if cached:
        return cached

    repo = get_repo()
    readme = repo.get_readme().decoded_content.decode()
    set_cached("readme", readme)
    return readme


def get_requirements():
    try:
        repo = get_repo()
        req = repo.get_contents("requirements.txt")
        return req.decoded_content.decode()
    except Exception:
        return None


# ------------------------------------------------------------
# METADATA
# ------------------------------------------------------------

def get_repo_metadata():
    repo = get_repo()
    return {
        "name": repo.name,
        "description": repo.description,
        "language": repo.language,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
    }


def get_owner_info():
    repo = get_repo()
    owner = repo.owner
    return f"""
Owner: {owner.login}
Profile: {owner.html_url}
Type: {owner.type}
"""


# ------------------------------------------------------------
# SUMMARY (LLM ALLOWED — README ONLY)
# ------------------------------------------------------------

def summarize_repo(readme: str, tree: list, metadata: dict) -> str:
    intro = _clean_readme(readme)

    summary = []

    # ---- Intro from README ----
    if intro:
        summary.append(intro)
    else:
        summary.append(
            f"{metadata['name']} is a software project written primarily "
            f"in {metadata.get('language', 'an unspecified language')}."
        )

    # ---- Structure ----
    summary.append("")
    summary.append("At a high level, the repository is organized as follows:")

    for item in tree:
        suffix = "/" if item["type"] == "dir" else ""
        summary.append(f"- {item['name']}{suffix}")

    # ---- Scope disclaimer ----
    summary.append("")
    summary.append(
        "This overview is based on the repository README and "
        "top-level file structure, not on internal code analysis."
    )

    return "\n".join(summary)
