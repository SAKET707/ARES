from utils.language_utils import detect_language_from_path
import ast



def detect_language(path: str) -> str:
    return detect_language_from_path(path)



def code_metrics(content: str, language: str) -> dict:
    if language != "python":
        raise NotImplementedError("Metrics only supported for Python")

    tree = ast.parse(content)

    return {
        "lines": len(content.splitlines()),
        "functions": sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree)),
        "classes": sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree)),
        "imports": sum(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree)),
    }


def format_metrics(metrics: dict) -> str:
    return "\n".join(f"{k}: {v}" for k, v in metrics.items())



def explain_code(content, language, llm, system_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
    ]
    return llm.invoke(messages).content


def explain_code_slice(content, language, start_line, end_line, llm, system_prompt):
    lines = content.splitlines()
    slice_content = "\n".join(lines[start_line - 1:end_line])

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": slice_content},
    ]
    return llm.invoke(messages).content
