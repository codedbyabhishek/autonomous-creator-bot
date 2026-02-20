# Autonomous Creator Bot

A starter repository for a self-directed bot that can:
- think through a goal,
- break it into steps,
- create project files automatically,
- review its own output,
- iterate for multiple rounds.

## What this bot does
Given a goal like:

```bash
python3 main.py "Create a simple portfolio website"
```

the bot will:
1. Generate a plan.
2. Execute actions (create/update files in a safe workspace).
3. Critique what it created.
4. Improve in the next iteration.

## Project structure

- `main.py`: CLI entrypoint
- `bot/planner.py`: Generates plans from goals
- `bot/runner.py`: Executes planned actions safely
- `bot/memory.py`: Stores past runs and learnings
- `bot/llm.py`: Optional OpenAI/Ollama reasoning layer with fallback mode

## Quick start

### 1) Run with local heuristic mode (no API key needed)

```bash
python3 main.py "Create a simple Flask app skeleton"
```

### 2) Run with OpenAI (optional)

```bash
export OPENAI_API_KEY="your_key"
python3 main.py "Create a Python package with tests" --use-llm --provider openai
```

### 3) Run with Ollama (free local model)

1. Install and start Ollama.
2. Pull a model (example):

```bash
ollama pull llama3.2:3b
```

3. Run:

```bash
python3 main.py "Create a Python package with tests" --use-llm --provider ollama
```

## Options

```bash
python3 main.py "your goal" \
  --workspace ./generated \
  --iterations 3 \
  --use-llm \
  --provider ollama \
  --ollama-model llama3.2:3b
```

- `--workspace`: where generated files go
- `--iterations`: number of think/build/review loops
- `--use-llm`: enables LLM planning
- `--provider`: `auto`, `openai`, or `ollama`
- `--ollama-model`: local model name for Ollama
- `--ollama-base-url`: Ollama API URL (default `http://127.0.0.1:11434`)

## Safety

The runner only writes inside the specified workspace directory and prevents path traversal.

## Notes

This is a solid base for your idea of a bot that can create things by itself. You can extend it with:
- web browsing tools,
- code execution sandboxing,
- richer tool plugins,
- long-term vector memory.
