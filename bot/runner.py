from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


class SafeRunner:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def _resolve_safe_path(self, relative_path: str) -> Path:
        target = (self.workspace / relative_path).resolve()
        if not str(target).startswith(str(self.workspace)):
            raise ValueError(f"Unsafe path blocked: {relative_path}")
        return target

    def execute(self, plan: List[Dict[str, Any]]) -> List[str]:
        written_files: List[str] = []
        for step in plan:
            if step.get("action") != "create_file":
                continue
            rel_path = step.get("path", "").strip()
            content = step.get("content", "")
            if not rel_path:
                continue

            target = self._resolve_safe_path(rel_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            written_files.append(rel_path)
        return written_files
