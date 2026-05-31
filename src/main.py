from __future__ import annotations

import logging
from typing import Any

from dotenv import load_dotenv
from langfuse import get_client


LOGGER = logging.getLogger(__name__)

USER_ID = "demo-user-001"
SESSION_ID = "demo-session-001"
MODEL_NAME = "gpt-4o-mini"
QUESTION = "How do I report nested spans with Langfuse Python SDK v3?"


def load_environment() -> None:
    """Load local environment variables from .env when present."""
    load_dotenv()


def build_prompt(user_context: dict[str, Any], question: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are a concise assistant. Use the user profile and answer "
                "with practical Langfuse SDK guidance."
            ),
        },
        {
            "role": "user",
            "content": (
                f"User tier: {user_context['tier']}. "
                f"Preferred language: {user_context['preferred_language']}. "
                f"Question: {question}"
            ),
        },
    ]


def simulate_llm_response(prompt: list[dict[str, str]]) -> str:
    if not prompt:
        raise ValueError("prompt must not be empty")

    return "Langfuse nested span demo completed."


def run_nested_span_demo(langfuse_client=None) -> dict[str, Any]:
    client = langfuse_client or get_client()
    result: dict[str, Any]

    with client.start_as_current_span(
        name="chat_request",
        input={"question": QUESTION},
        metadata={"entrypoint": "src.main"},
    ) as root_span:

        client.update_current_trace(
            name="langfuse-python-sdk-nested-spans-demo",
            user_id=USER_ID,
            session_id=SESSION_ID,
            input={"question": QUESTION},
            version="1.0.0",
            tags=["python-sdk-v3", "nested-spans", "demo"],
            metadata={
                "plan": "nested-spans-demo",
                "user_email_hash": "demo-user-email-hash",
            },
        )

        with client.start_as_current_span(
            name="load_user_context",
            input={"user_id": USER_ID},
        ) as user_context_span:
            user_context_span.update_trace(name="user_context_span",
                                           user_id=1000,
                                           session_id=1000,
                                           tags=["user-context", "demo"])
            user_context = {
                "user_id": USER_ID,
                "tier": "pro",
                "preferred_language": "zh-CN",
            }
            user_context_span.update(output=user_context)

        with client.start_as_current_span(
            name="build_prompt",
            input={"question": QUESTION, "user_context": user_context},
        ) as prompt_span:
            prompt = build_prompt(user_context, QUESTION)
            prompt_span.update(output={"messages": len(prompt)})

        with client.start_as_current_observation(
            name="llm_completion",
            as_type="generation",
            model=MODEL_NAME,
            model_parameters={
                "temperature": 0.2,
                "max_tokens": 128,
            },
            input=prompt,
            usage_details={
                "input": 42,
                "output": 12,
                "total": 54,
            },
        ) as generation:
            answer = simulate_llm_response(prompt)
            generation.update(output=answer)

        result = {
            "answer": answer,
            "user_id": USER_ID,
            "model": MODEL_NAME,
        }
        root_span.update(output=result, metadata={"status": "completed"})

    client.flush()
    return result


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    load_environment()
    result = run_nested_span_demo()
    LOGGER.info("Langfuse nested span demo finished for user_id=%s model=%s", USER_ID, result["model"])


if __name__ == "__main__":
    main()
