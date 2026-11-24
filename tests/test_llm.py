"""Tests of the OpenAI-compatible client `founder_vn.llm` against the fake provider."""

import pytest
from conftest import FakeProvider

from founder_vn import llm

ENV = ("FOUNDER_LLM_BASE_URL", "FOUNDER_LLM_API_KEY", "FOUNDER_LLM_MODEL")


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV:
        monkeypatch.delenv(name, raising=False)


def _configure(monkeypatch: pytest.MonkeyPatch, provider: FakeProvider) -> None:
    monkeypatch.setenv("FOUNDER_LLM_BASE_URL", provider.base_url)
    monkeypatch.setenv("FOUNDER_LLM_API_KEY", "khoa-gia")
    monkeypatch.setenv("FOUNDER_LLM_MODEL", "mo-hinh-gia")


def test_unconfigured_names_every_missing_variable_and_has_no_default() -> None:
    with pytest.raises(llm.NotConfigured) as caught:
        llm.load_config()
    message = str(caught.value)
    for name in ENV:
        assert name in message


def test_partly_configured_names_only_the_missing_ones(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FOUNDER_LLM_MODEL", "mo-hinh-gia")
    with pytest.raises(llm.NotConfigured) as caught:
        llm.load_config()
    first_line = str(caught.value).splitlines()[0]
    assert "FOUNDER_LLM_BASE_URL" in first_line
    assert "FOUNDER_LLM_API_KEY" in first_line
    assert "FOUNDER_LLM_MODEL" not in first_line


def test_complete_returns_the_reply_and_sends_only_model_and_messages(
    monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _configure(monkeypatch, fake_provider)
    fake_provider.reply = "đã nhận"
    assert llm.complete(llm.load_config(), "chào", timeout=5) == "đã nhận"
    (body,) = fake_provider.requests
    assert body == {"model": "mo-hinh-gia", "messages": [{"role": "user", "content": "chào"}]}
    assert fake_provider.headers[0]["Authorization"] == "Bearer khoa-gia"


def test_complete_with_usage_returns_text_tokens_and_latency_from_the_same_call(
    monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _configure(monkeypatch, fake_provider)
    fake_provider.reply = "đã nhận"
    fake_provider.usage = (123, 45)
    fake_provider.script = lambda body, n: (200, "đã nhận", 0.05)
    reply = llm.complete_with_usage(llm.load_config(), "chào", timeout=5)
    assert reply.content == "đã nhận"
    assert (reply.prompt_tokens, reply.completion_tokens) == (123, 45)
    assert reply.seconds >= 0.05
    (body,) = fake_provider.requests
    assert body == {"model": "mo-hinh-gia", "messages": [{"role": "user", "content": "chào"}]}


def test_complete_with_usage_tolerates_a_reply_without_usage(
    monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _configure(monkeypatch, fake_provider)
    fake_provider.usage = None
    reply = llm.complete_with_usage(llm.load_config(), "chào", timeout=5)
    assert reply.content == "xin chào"
    assert (reply.prompt_tokens, reply.completion_tokens) == (None, None)
