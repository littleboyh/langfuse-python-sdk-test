# Langfuse Python SDK Nested Spans Demo

This repository contains a minimal Langfuse Python SDK v3 example that reports:

- a root `chat_request` span
- nested `load_user_context` and `build_prompt` spans
- a nested `llm_completion` generation with model metadata
- trace-level user and session metadata

## Prerequisites

- Python 3.12
- uv 0.11+
- A Langfuse project, either on Langfuse Cloud or a local/self-hosted Langfuse instance

Check uv:

```bash
uv --version
```

## Quick Start

1. Create `.env` from the example file:

```powershell
Copy-Item .env.example .env
```

2. Edit `.env` and set your own Langfuse credentials:

```bash
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

For local Langfuse, use your local URL instead:

```bash
LANGFUSE_BASE_URL=http://127.0.0.1:3000
```

3. Install dependencies:

```bash
uv sync
```

4. Start the demo:

```bash
uv run python -m src.main
```

The script sends a trace named `langfuse-python-sdk-nested-spans-demo` to Langfuse. Open your Langfuse project UI and check the traces page after the command finishes.

5. Run tests:

```bash
uv run pytest -v
```

## Common uv Commands

Sync the virtual environment from `pyproject.toml` and `uv.lock`:

```bash
uv sync
```

Run the project:

```bash
uv run python -m src.main
```

Run tests:

```bash
uv run pytest -v
```

Add a runtime dependency:

```bash
uv add "package-name"
```

Add a development dependency:

```bash
uv add --dev "package-name"
```

Update the lockfile:

```bash
uv lock
```

## Version Note

PyPI does not publish a `langfuse==3.174.1` Python SDK package. This project depends on `langfuse>=3,<4`, which keeps the Python SDK on the v3 line for Langfuse v3 server deployments.
