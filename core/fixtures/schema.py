"""Контракт, по которому schemathesis генерирует проверки."""
import pytest
import schemathesis

from core.settings import BASE_DIR, Settings


@pytest.fixture(scope="session")
def api_schema(settings: Settings):
    """Схема OpenAPI: с диска (openapi_path) либо со стенда (openapi_url)."""
    if settings.openapi_path:
        path = (BASE_DIR / settings.openapi_path).resolve()
        schema = schemathesis.openapi.from_path(str(path))
    elif settings.openapi_url:
        schema = schemathesis.openapi.from_url(
            settings.openapi_url,
            headers={"Authorization": f"Bearer {settings.api_token}"} if settings.api_token else None,
        )
    else:
        raise RuntimeError("Не задан ни openapi_path, ни openapi_url в settings.toml")

    schema.base_url = settings.api_base_url.rstrip("/")
    return schema
