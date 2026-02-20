from __future__ import annotations

from typing import Any, Dict, List

from .llm import LLMReasoner


class Planner:
    def __init__(self, use_llm: bool = False) -> None:
        self.reasoner = LLMReasoner(enabled=use_llm)

    def build_plan(self, goal: str, previous_critique: str = "") -> List[Dict[str, Any]]:
        result = self.reasoner.think(goal, previous_critique)
        plan = result.get("plan", [])
        return [item for item in plan if item.get("action") == "create_file"]

    def critique(self, goal: str, produced_files: List[str]) -> str:
        missing_core = "README.md" not in produced_files
        if missing_core:
            return f"For goal '{goal}', include README.md for usage context."
        return "Output includes core project files; next round can improve quality and tests."
