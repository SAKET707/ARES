# intents/classifier.py
import re
import json
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from config.prompts import INTENT_CLASSIFIER_PROMPT


# -------------------------------------------------------------------
# INTENT ENUM (SOURCE OF TRUTH)
# -------------------------------------------------------------------

class Intent(str, Enum):
    SHOW_REPO_TREE = "SHOW_REPO_TREE"
    SHOW_FILE_CODE = "SHOW_FILE_CODE"
    EXPLAIN_CODE = "EXPLAIN_CODE"
    EXPLAIN_CODE_SLICE = "EXPLAIN_CODE_SLICE"
    CODE_METRICS = "CODE_METRICS"
    DEPENDENCY_GRAPH = "DEPENDENCY_GRAPH"
    REPO_SUMMARY = "REPO_SUMMARY"
    GET_OWNER_INFO = "GET_OWNER_INFO"


# -------------------------------------------------------------------
# ENTITY SCHEMA
# -------------------------------------------------------------------

class IntentEntities(BaseModel):
    filename: Optional[str] = Field(
        default=None,
        description="Exact filename if mentioned, else null"
    )
    start_line: Optional[int] = Field(
        default=None,
        description="Start line number for code slice"
    )
    end_line: Optional[int] = Field(
        default=None,
        description="End line number for code slice"
    )


class IntentResult(BaseModel):
    intent: Intent
    entities: IntentEntities


# -------------------------------------------------------------------
# INTENT CLASSIFIER
# -------------------------------------------------------------------


def _extract_json(text: str) -> dict:
    """
    Extract the first JSON object found in text.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in LLM output")
    return json.loads(match.group())


def classify_intent(llm, user_query: str) -> IntentResult:
    messages = [
        {"role": "system", "content": INTENT_CLASSIFIER_PROMPT},
        {"role": "user", "content": user_query},
    ]

    response = llm.invoke(messages)
    raw = response.content

    try:
        # Case 1: already parsed dict
        if isinstance(raw, dict):
            data = raw

        # Case 2: list of blocks
        elif isinstance(raw, list):
            text = "".join(
                part.get("text", "")
                for part in raw
                if isinstance(part, dict)
            )
            data = _extract_json(text)

        # Case 3: string (may include prose or be empty)
        elif isinstance(raw, str):
            if not raw.strip():
                raise ValueError("Empty LLM response")
            data = _extract_json(raw)

        else:
            raise TypeError(f"Unsupported response.content type: {type(raw)}")

        return IntentResult.model_validate(data)

    except Exception as e:
        raise ValueError(
            f"Intent classification failed.\nRaw output:\n{raw}"
        ) from e




