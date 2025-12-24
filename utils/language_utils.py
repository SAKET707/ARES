
import os


_EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".md": "markdown",
}


def detect_language_from_path(path: str) -> str:
    _, ext = os.path.splitext(path.lower())
    return _EXTENSION_LANGUAGE_MAP.get(ext, "unknown")
