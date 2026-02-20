from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class RunRecord:
    timestamp: str
    goal: str
    plan: List[Dict[str, Any]]
    critique: str


class MemoryStore:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.base_dir / "memory.json"

    def load(self) -> List[Dict[str, Any]]:
        if not self.file_path.exists():
            return []
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def save_run(self, goal: str, plan: List[Dict[str, Any]], critique: str) -> None:
        history = self.load()
        record = RunRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            goal=goal,
            plan=plan,
            critique=critique,
        )
        history.append(asdict(record))
        self.file_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
