"""Аутентификация тестов: логин, токен и заголовки к API.

Токен живёт `expires_in=1800` (30 минут), тогда как прогон api-набора — около
часа, поэтому здесь же точка пересборки токена: waiter при 401 просит свежие
заголовки через set_auth_refresher().
"""
from __future__ import annotations

import logging
import time

import pytest
import requests

from core.helpers.waiter import RETRY_STATUSES
from core.settings import Settings

LOG = logging.getLogger(__name__)

TOKEN_RETRIES = 3
TOKEN_RETRY_WAIT_S = 2.0


def _post_token(base_url: str, username: str, password: str) -> dict:
    """POST /api/v1/token с повторами на 408/429/5xx и сетевых ошибках.

    Стенд иногда отвечает 408 на сам логин; с одним-единственным запросом
    вся сессия стартовала бы либо падением, либо пропуском всего набора.
    """
    data = {"grant_type": "password", "username": username, "password": password}
    url = f"{base_url.rstrip('/')}/api/v1/token"
    last = None
    for attempt in range(1, TOKEN_RETRIES + 1):
        try:
            resp = requests.post(url, data=data, timeout=(5, 20))
        except requests.RequestException as exc:
            last = f"{type(exc).__name__}: {exc}"
        else:
            if resp.status_code not in RETRY_STATUSES and resp.status_code < 500:
                resp.raise_for_status()
                return resp.json()
            last = f"HTTP {resp.status_code}"
        if attempt < TOKEN_RETRIES:
            wait = TOKEN_RETRY_WAIT_S * attempt
            LOG.warning("логин: %s — попытка %d/%d, жду %ss", last, attempt, TOKEN_RETRIES, wait)
            time.sleep(wait)
    raise RuntimeError(f"не удалось получить токен с {url} после {TOKEN_RETRIES} попыток: {last}")


def obtain_access_token(settings: Settings) -> str:
    """Логинит settings.username/password и сохраняет токен в settings."""
    if not settings.username or not settings.password:
        return ""
    payload = _post_token(settings.api_base_url, settings.username, settings.password)
    token = payload["access_token"]
    settings.api_token = token
    settings.token_type = payload.get("token_type", "bearer")
    settings.refresh_token = payload.get("refresh_token")
    return token


def auth_header(settings: Settings) -> dict[str, str]:
    """Заголовки запроса к API; при отсутствии токена — логинется."""
    if not settings.api_token:
        obtain_access_token(settings)
    if not settings.api_token:
        raise RuntimeError("ни api_token, ни username/password — нечем аутентифицироваться")
    return settings.auth_header()


@pytest.fixture(scope="session")
def auth_headers(settings: Settings) -> dict:
    if not settings.api_token and not (settings.username and settings.password):
        pytest.skip("No api_token and no credentials in settings — cannot authenticate")
    return auth_header(settings)


@pytest.fixture
def require_token(settings: Settings):
    """Скипает тест, если токен не задан в settings."""
    if not settings.api_token:
        pytest.skip("api_token is not set in settings")
