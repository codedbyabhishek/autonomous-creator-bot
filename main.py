from __future__ import annotations

import argparse
from pathlib import Path

from bot.memory import MemoryStore
from bot.planner import Planner
from bot.runner import SafeRunner


def run(goal: str, workspace: Path, iterations: int, use_llm: bool) -> None:
    planner = Planner(use_llm=use_llm)
    runner = SafeRunner(workspace=workspace)
    memory = MemoryStore(base_dir=workspace / ".runs")

    critique = ""
    for i in range(1, iterations + 1):
        plan = planner.build_plan(goal, critique)
        written = runner.execute(plan)
        critique = planner.critique(goal, written)
        memory.save_run(goal=goal, plan=plan, critique=critique)

        print(f"\\nIteration {i}/{iterations}")
        print(f"Wrote files: {', '.join(written) if written else 'none'}")
        print(f"Critique: {critique}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Autonomous Creator Bot")
    parser.add_argument("goal", help="High-level project goal")
    parser.add_argument(
        "--workspace",
        default="generated",
        help="Output folder for generated project files",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=2,
        help="Number of autonomous think/build/review loops",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use OpenAI if OPENAI_API_KEY is configured",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(
        goal=args.goal,
        workspace=Path(args.workspace),
        iterations=max(1, args.iterations),
        use_llm=args.use_llm,
    )
