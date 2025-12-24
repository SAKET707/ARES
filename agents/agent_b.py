# agents/agent_b.py

from tools import file_tools, code_tools, dependency_tools
from config.prompts import AGENT_B_SYSTEM_PROMPT


class AgentB:
    """
    Code / Technical Agent
    """

    def __init__(self, llm):
        self.llm = llm

    # ------------------------------------------------------------
    # FILE DISPLAY
    # ------------------------------------------------------------

    def show_file(self, path: str) -> str:
        content = file_tools.get_file_content(path)
        return content

    # ------------------------------------------------------------
    # CODE EXPLANATION
    # ------------------------------------------------------------

    def explain_file(self, path: str) -> str:
        content = file_tools.get_file_content(path)
        language = code_tools.detect_language(path)

        explanation = code_tools.explain_code(
            content=content,
            language=language,
            llm=self.llm,
            system_prompt=AGENT_B_SYSTEM_PROMPT,
        )
        return explanation

    def explain_file_slice(
        self,
        path: str,
        start_line: int,
        end_line: int,
    ) -> str:
        content = file_tools.get_file_content(path)
        language = code_tools.detect_language(path)

        explanation = code_tools.explain_code_slice(
            content=content,
            language=language,
            start_line=start_line,
            end_line=end_line,
            llm=self.llm,
            system_prompt=AGENT_B_SYSTEM_PROMPT,
        )
        return explanation

    # ------------------------------------------------------------
    # METRICS
    # ------------------------------------------------------------

    def code_metrics(self, path: str) -> str:
        content = file_tools.get_file_content(path)
        language = code_tools.detect_language(path)
        metrics = code_tools.code_metrics(content, language)
        return code_tools.format_metrics(metrics)

    # ------------------------------------------------------------
    # DEPENDENCIES
    # ------------------------------------------------------------

    def dependency_graph(self, path: str) -> str:
        content = file_tools.get_file_content(path)
        language = code_tools.detect_language(path)

        imports = dependency_tools.extract_imports(content, language)
        graph = dependency_tools.build_dependency_graph(imports)
        return dependency_tools.format_dependency_graph(graph)
