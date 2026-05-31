from contextlib import AbstractContextManager

from src.main import run_nested_span_demo


class FakeObservation(AbstractContextManager):
    def __init__(self, client, kind, kwargs):
        self.client = client
        self.kind = kind
        self.kwargs = kwargs
        self.updates = []

    def __enter__(self):
        self.client.events.append(("enter", self.kind, self.kwargs))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.events.append(("exit", self.kind, self.kwargs["name"]))
        return False

    def update(self, **kwargs):
        self.updates.append(kwargs)
        self.client.events.append(("update_observation", self.kind, kwargs))

    def update_trace(self, **kwargs):
        self.client.events.append(("update_observation_trace", self.kind, kwargs))


class FakeLangfuseClient:
    def __init__(self):
        self.events = []
        self.trace_updates = []
        self.flushed = False

    def start_as_current_span(self, **kwargs):
        return FakeObservation(self, "span", kwargs)

    def start_as_current_observation(self, **kwargs):
        return FakeObservation(self, "generation", kwargs)

    def update_current_trace(self, **kwargs):
        self.trace_updates.append(kwargs)
        self.events.append(("update_trace", kwargs))

    def flush(self):
        self.flushed = True
        self.events.append(("flush",))


def test_run_nested_span_demo_reports_nested_spans_user_and_model():
    client = FakeLangfuseClient()

    result = run_nested_span_demo(client)

    assert result["answer"] == "Langfuse nested span demo completed."
    assert [event[2]["name"] for event in client.events if event[0] == "enter"] == [
        "chat_request",
        "load_user_context",
        "build_prompt",
        "llm_completion",
    ]
    assert client.trace_updates[0]["user_id"] == "demo-user-001"
    assert client.trace_updates[0]["session_id"] == "demo-session-001"
    assert client.trace_updates[0]["metadata"]["plan"] == "nested-spans-demo"

    generation_event = next(
        event for event in client.events if event[0] == "enter" and event[1] == "generation"
    )
    assert generation_event[2]["as_type"] == "generation"
    assert generation_event[2]["model"] == "gpt-4o-mini"
    assert generation_event[2]["model_parameters"] == {
        "temperature": 0.2,
        "max_tokens": 128,
    }
    assert generation_event[2]["usage_details"] == {
        "input": 42,
        "output": 12,
        "total": 54,
    }

    root_update = next(
        event
        for event in client.events
        if event[0] == "update_observation"
        and event[1] == "span"
        and event[2].get("output") == result
    )
    assert root_update[2]["metadata"]["status"] == "completed"
    assert client.flushed is True
