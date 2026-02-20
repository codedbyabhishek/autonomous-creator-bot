from __future__ import annotations

import argparse
from pathlib import Path

from bot.memory import MemoryStore
from bot.planner import Planner
from bot.runner import SafeRunner


def run(
    goal: str,
    workspace: Path,
    iterations: int,
    use_llm: bool,
    provider: str,
    ollama_model: str,
    ollama_base_url: str,
) -> None:
    planner = Planner(
        use_llm=use_llm,
        provider=provider,
        ollama_model=ollama_model,
        ollama_base_url=ollama_base_url,
    )
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
        help="Use LLM reasoning (OpenAI or local Ollama)",
    )
    parser.add_argument(
        "--provider",
        choices=["auto", "openai", "ollama"],
        default="auto",
        help="LLM provider: auto, openai, or ollama",
    )
    parser.add_argument(
        "--ollama-model",
        default="llama3.2:3b",
        help="Ollama model name (used when provider is ollama/auto)",
    )
    parser.add_argument(
        "--ollama-base-url",
        default="http://127.0.0.1:11434",
        help="Ollama API base URL",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(
        goal=args.goal,
        workspace=Path(args.workspace),
        iterations=max(1, args.iterations),
        use_llm=args.use_llm,
        provider=args.provider,
        ollama_model=args.ollama_model,
        ollama_base_url=args.ollama_base_url,
    )
