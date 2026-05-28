# Langfuse Python SDK Nested Spans Demo

This repository contains a minimal Langfuse Python SDK v3 example that reports:

- a root `chat_request` span
- nested `load_user_context` and `build_prompt` spans
- a nested `llm_completion` generation with model metadata
- trace-level user and session metadata

## Setup

Create `.env` with your Langfuse credentials:

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the demo:

```bash
python -m src.main
```

Run tests:

```bash
python -m pytest -v
```

## Version Note

PyPI does not publish a `langfuse==3.174.1` Python SDK package. This project depends on `langfuse>=3,<4`, which keeps the Python SDK on the v3 line for Langfuse v3 server deployments.
