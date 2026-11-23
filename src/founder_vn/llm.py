"""The one OpenAI-compatible client behind ``panel run``.

Configured by ``FOUNDER_LLM_BASE_URL``, ``FOUNDER_LLM_API_KEY`` and ``FOUNDER_LLM_MODEL``; there
is no default provider. The request carries only ``model`` and ``messages``: nothing relies on
``response_format``, ``seed`` or ``temperature``, so the caller extracts and validates JSON itself.
"""

import os
from collections.abc import Mapping
from dataclasses import dataclass

import httpx

ENV_NAMES = ("FOUNDER_LLM_BASE_URL", "FOUNDER_LLM_API_KEY", "FOUNDER_LLM_MODEL")
TIMEOUT = 90.0
SETUP = (
    "Đặt ba biến môi trường trước khi chạy: FOUNDER_LLM_BASE_URL (địa chỉ gốc của máy chủ tương "
    "thích OpenAI, ví dụ https://<máy-chủ>/v1), FOUNDER_LLM_API_KEY (khoá truy cập) và "
    "FOUNDER_LLM_MODEL (tên mô hình). Không có nhà cung cấp mặc định. / Set these three "
    "environment variables for the MCP server or the shell: the base URL of an OpenAI-compatible "
    "server, its API key and the model name; there is no default provider."
)


class NotConfigured(ValueError):
    """A ``FOUNDER_LLM_*`` variable is missing; the message names it and says how to set up."""


class CallFailed(RuntimeError):
    """One model call failed (timeout, connection, HTTP error or unreadable reply)."""


@dataclass(frozen=True)
class Config:
    base_url: str
    api_key: str
    model: str


def load_config(env: Mapping[str, str] | None = None) -> Config:
    """Read the three variables; raise ``NotConfigured`` naming each missing one."""
    source = os.environ if env is None else env
    values = {name: source.get(name, "").strip() for name in ENV_NAMES}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise NotConfigured(f"chưa cấu hình mô hình, thiếu {', '.join(missing)}. {SETUP}")
    return Config(*(values[name] for name in ENV_NAMES))


def complete(config: Config, prompt: str, timeout: float = TIMEOUT) -> str:
    """Send ``prompt`` as one user message; return the reply text or raise ``CallFailed``."""
    url = config.base_url.rstrip("/") + "/chat/completions"
    body = {"model": config.model, "messages": [{"role": "user", "content": prompt}]}
    try:
        response = httpx.post(
            url,
            json=body,
            headers={"Authorization": f"Bearer {config.api_key}"},
            timeout=timeout,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
    except httpx.TimeoutException:
        raise CallFailed(f"quá thời gian chờ {timeout:g} giây") from None
    except httpx.HTTPStatusError as e:
        raise CallFailed(f"máy chủ mô hình trả mã {e.response.status_code}") from None
    except httpx.HTTPError as e:
        raise CallFailed(f"không gọi được máy chủ mô hình: {type(e).__name__}") from None
    except (ValueError, KeyError, IndexError, TypeError):
        raise CallFailed("câu trả lời của máy chủ mô hình không đọc được") from None
    if not isinstance(content, str):
        raise CallFailed("câu trả lời của máy chủ mô hình không có nội dung chữ")
    return content
