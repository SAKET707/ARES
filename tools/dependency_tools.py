# tools/dependency_tools.py

import ast


def extract_imports(content: str, language: str):
    if language != "python":
        raise NotImplementedError("Dependency extraction only supports Python")

    tree = ast.parse(content)
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])

    return sorted(imports)


def build_dependency_graph(imports):
    return {
        "direct_dependencies": imports
    }


def format_dependency_graph(graph):
    lines = ["Direct dependencies:"]
    for dep in graph["direct_dependencies"]:
        lines.append(f"- {dep}")
    return "\n".join(lines)
