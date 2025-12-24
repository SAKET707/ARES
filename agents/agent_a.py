from intents.classifier import classify_intent, Intent
from tools import repo_tools
from agents.agent_b import AgentB


class AgentA:
    """
    Leader / Router Agent
    """

    def __init__(self, llm):
        self.llm = llm
        self.agent_b = AgentB(llm)

    def handle_query(self, user_query: str) -> str:
        """
        Main entry point for all user queries.
        """

        intent_result = classify_intent(self.llm, user_query)
        intent = intent_result.intent
        entities = intent_result.entities

        if intent == Intent.SHOW_REPO_TREE:
            return self._show_repo_tree()

        if intent == Intent.REPO_SUMMARY:
            return self._repo_summary()

        if intent == Intent.GET_OWNER_INFO:
            return self._get_owner_info()

        if intent == Intent.SHOW_FILE_CODE:
            return self._show_file_code(entities.filename)

        if intent == Intent.EXPLAIN_CODE:
            return self._explain_file(entities.filename)

        if intent == Intent.EXPLAIN_CODE_SLICE:
            return self._explain_code_slice(
                entities.filename,
                entities.start_line,
                entities.end_line,
            )

        if intent == Intent.CODE_METRICS:
            return self._code_metrics(entities.filename)

        if intent == Intent.DEPENDENCY_GRAPH:
            return self._dependency_graph(entities.filename)

        raise ValueError(f"Unhandled intent: {intent}")


    def _show_repo_tree(self) -> str:
        tree = repo_tools.get_repo_tree()
        metadata = repo_tools.get_repo_metadata()

        lines = [f"{metadata['name']}/"]
        lines.extend(repo_tools.format_repo_tree(tree))

        return "\n".join(lines)


    def _repo_summary(self) -> str:
        readme = repo_tools.get_readme()
        tree = repo_tools.get_repo_tree()
        metadata = repo_tools.get_repo_metadata()
        return repo_tools.summarize_repo(readme, tree, metadata)

    def _get_owner_info(self) -> str:
        return repo_tools.get_owner_info()

    def _show_file_code(self, filename: str) -> str:
        path = self._resolve_file_path(filename)
        return self.agent_b.show_file(path)

    def _explain_file(self, filename: str) -> str:
        path = self._resolve_file_path(filename)
        return self.agent_b.explain_file(path)

    def _explain_code_slice(
        self,
        filename: str,
        start_line: int,
        end_line: int,
    ) -> str:
        if start_line is None or end_line is None:
            raise ValueError("Line range required for code slice explanation")

        path = self._resolve_file_path(filename)
        return self.agent_b.explain_file_slice(path, start_line, end_line)

    def _code_metrics(self, filename: str) -> str:
        path = self._resolve_file_path(filename)
        return self.agent_b.code_metrics(path)

    def _dependency_graph(self, filename: str) -> str:
        path = self._resolve_file_path(filename)
        return self.agent_b.dependency_graph(path)


    def _resolve_file_path(self, filename: str) -> str:
        if not filename:
            raise ValueError("Filename not provided")

        matches = repo_tools.find_file_path(filename)

        if not matches:
            raise FileNotFoundError(f"File '{filename}' not found in repository")

        if len(matches) > 1:
            options = "\n".join(matches)
            raise ValueError(
                f"Multiple files named '{filename}' found:\n{options}"
            )

        return matches[0]
