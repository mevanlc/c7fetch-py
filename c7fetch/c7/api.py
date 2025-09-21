from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from c7fetch.cli import settings

BASE_URL = "https://context7.com/api/v1"
_TIMEOUT = 30
_LAST_REQUEST_TS: float = 0.0


class ApiError(Exception):
    """Base exception for Context7 API issues."""

    def __init__(self, message: str, *, status: Optional[int] = None):
        super().__init__(message)
        self.status = status


class MissingApiKey(ApiError):
    pass


class HttpError(ApiError):
    pass


@dataclass
class FetchResponse:
    payload: Any
    content_type: str


def _rate_limit_delay() -> None:
    global _LAST_REQUEST_TS
    delay_ms = settings.get_setting("request_delay")
    try:
        delay_seconds = max(int(delay_ms), 0) / 1000.0
    except (TypeError, ValueError):
        delay_seconds = 0.0

    if delay_seconds <= 0:
        return

    now = time.monotonic()
    elapsed = now - _LAST_REQUEST_TS if _LAST_REQUEST_TS else None
    if elapsed is not None and elapsed < delay_seconds:
        time.sleep(delay_seconds - elapsed)
    _LAST_REQUEST_TS = time.monotonic()


def _resolve_api_key() -> str:
    env_var = settings.get_setting("apikey_env")
    if env_var:
        candidate = os.getenv(env_var)
        if candidate:
            return candidate
    key = settings.get_setting("apikey")
    if key:
        return key
    raise MissingApiKey(
        "Context7 API key is not configured. Use config set or environment variable."
    )


def is_api_key_configured() -> bool:
    """Return True if an API key is discoverable via config or environment."""
    env_var = settings.get_setting("apikey_env")
    if env_var:
        candidate = os.getenv(env_var)
        if candidate:
            return True
    key = settings.get_setting("apikey")
    return bool(key)


def _base_headers() -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {_resolve_api_key()}",
        "User-Agent": settings.get_setting("user_agent") or "c7fetch/0.0.0",
    }
    return headers


def _request(
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    accept: str = "application/json",
) -> requests.Response:
    _rate_limit_delay()
    url = f"{BASE_URL}/{path.lstrip('/')}"
    headers = _base_headers()
    headers["Accept"] = accept
    try:
        response = requests.get(url, params=params, headers=headers, timeout=_TIMEOUT)
    except requests.RequestException as exc:
        raise ApiError(f"Failed to call Context7 API: {exc}") from exc

    if response.status_code == 401:
        raise MissingApiKey("Context7 API rejected credentials (401 Unauthorized).")
    if response.status_code == 429:
        raise HttpError(
            "Context7 API rate limit reached (429). Retry after a delay.", status=429
        )
    if not response.ok:
        snippet = response.text[:200]
        raise HttpError(
            f"Context7 API request failed with status {response.status_code}: {snippet}",
            status=response.status_code,
        )
    return response


def search(query: str) -> Dict[str, Any]:
    """Execute a search request against Context7."""
    if not query:
        raise ValueError("Query must not be empty.")
    response = _request("search", params={"query": query})
    try:
        return response.json()
    except ValueError as exc:
        raise ApiError(
            "Context7 API returned invalid JSON for search response."
        ) from exc


def fetch(
    library_id: str,
    *,
    tokens: Optional[int] = None,
    format: str = "text",
    topic: Optional[str] = None,
) -> FetchResponse:
    if not library_id:
        raise ValueError("library_id must not be empty.")

    params: Dict[str, Any] = {}
    if format not in {"text", "json"}:
        raise ValueError("format must be either 'text' or 'json'.")
    params["type"] = format
    if tokens:
        params["tokens"] = tokens
    if topic:
        params["topic"] = topic

    accept = "application/json" if format == "json" else "text/markdown"
    response = _request(library_id, params=params, accept=accept)

    if format == "json":
        try:
            payload = response.json()
        except ValueError as exc:
            raise ApiError(
                "Context7 API returned invalid JSON for fetch response."
            ) from exc
        return FetchResponse(payload=payload, content_type="application/json")
    return FetchResponse(payload=response.text, content_type="text/markdown")
