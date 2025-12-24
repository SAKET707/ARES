
def format_error(message: str) -> str:
    return f"❌ Error: {message}"


def format_warning(message: str) -> str:
    return f"⚠️ Warning: {message}"


def format_section(title: str, body: str) -> str:
    line = "-" * len(title)
    return f"{title}\n{line}\n{body}"
