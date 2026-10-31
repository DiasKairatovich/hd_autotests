pytest_plugins = ["core.fixtures.auth", "core.fixtures.schema"]

from hypothesis import settings as hy_settings, HealthCheck, Phase

hy_settings.register_profile(
    "dev",
    hy_settings(
        phases=(Phase.explicit,),
        max_examples=1,
        deadline=None,
        suppress_health_check=[HealthCheck.too_slow],
    ),
)
hy_settings.load_profile("dev")

import pytest
from core.clients.api_client import APIClient
from core.settings import Settings, load_settings


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="окружение из configs/settings.toml: dev|stage",
    )
    parser.addoption("--log", action="store_true", default=False)
    parser.addoption(
        "--cleanup",
        action="store_true",
        default=False,
        help="удалить тестовые данные, оставшиеся от прошлых прогонов, до начала тестов",
    )
    parser.addoption(
        "--cleanup-prefix",
        action="append",
        dest="cleanup_prefix",
        default=None,
        help="префикс имени тестовой сущности (E2E_, UI_, ...); можно повторять",
    )
    parser.addoption(
        "--cleanup-only",
        dest="cleanup_only",
        default=None,
        help="ограничить зачистку списком сущностей через запятую: cameras,places",
    )
    parser.addoption(
        "--cleanup-dry-run",
        dest="cleanup_dry_run",
        action="store_true",
        default=False,
        help="только найти и показать мусор, ничего не удаляя",
    )


def pytest_configure(config):
    if config.getoption("--log"):
        config.option.log_cli = True
        config.option.log_cli_level = "INFO"


def pytest_collection_modifyitems(session, config, items):
    """--cleanup: подметаем остатки прошлых прогонов до первого теста."""
    if not config.getoption("--cleanup"):
        return
    from core.helpers.cleanup import cleanup_from_pytest_config

    cleanup_from_pytest_config(config)


@pytest.fixture(scope="session")
def settings(request) -> Settings:
    """Конфигурация стенда: configs/settings.toml + переменные из .env."""
    return load_settings(request.config.getoption("--env"))


@pytest.fixture(scope="session", autouse=True)
def api_resilience(request):
    """Обвязка устойчивости API-вызовов: чем пересобирать токен и когда
    закрывать общий keep-alive сеанс.

    Сами повторы (5xx/429/408/401/сетевые ошибки) живут в core/helpers/waiter.py;
    здесь лишь источник свежего токена: expires_in=1800, а прогон api-набора
    длится дольше получаса — на 401 нужно пересобрать токен, а не уводить тесты
    в «мёртвую сессию».
    """
    from core.helpers import waiter

    def _refresh() -> dict | None:
        from core.fixtures.auth import obtain_access_token

        settings = request.getfixturevalue("settings")
        auth_headers = request.getfixturevalue("auth_headers")
        token = obtain_access_token(settings)
        if not token:
            return None
        fresh = settings.auth_header(token)
        auth_headers.update(fresh)
        return fresh

    waiter.set_auth_refresher(_refresh)
    yield
    waiter.set_auth_refresher(None)
    waiter.close_http_session()


def pytest_terminal_summary(terminalreporter, *args, **kwargs):
    """Нестабильные тесты не должны прятаться за успешным PASSED."""
    from core.helpers.waiter import flaky_summary

    flaky = flaky_summary()
    if not flaky:
        return
    spent = sum(item["spent_s"] for item in flaky)
    terminalreporter.write_line("")
    terminalreporter.write_line(
        f"Нестабильные тесты: {len(flaky)} прошли только после повторов "
        f"(+{spent:.0f}s к длительности прогона):",
        yellow=True,
    )
    for item in sorted(flaky, key=lambda i: -i["spent_s"])[:15]:
        terminalreporter.write_line(
            f"  {item['operation']}: {item['attempts']} попыток, {item['spent_s']}s",
            yellow=True,
        )


@pytest.fixture(scope="session")
def api_client(settings, auth_headers):
    from core.fixtures.auth import obtain_access_token

    def _token_refresher() -> str:
        return obtain_access_token(settings)

    return APIClient(
        base_url=settings.api_base_url,
        headers=auth_headers,
        token_refresher=_token_refresher
    )

@pytest.fixture(scope="session")
def unauth_api_client(settings):
    """Provides an unauthenticated API client for negative testing."""
    return APIClient(base_url=settings.api_base_url)


@pytest.fixture
def created_group(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/groups", json=payload)
        if resp.status_code in (200, 201):
            gid = resp.json().get("id")
            if gid is not None:
                ids.append(gid)
        return resp

    yield _factory

    for gid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/groups/{gid}")
        except Exception:
            pass


@pytest.fixture
def created_place(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/places", json=payload)
        if resp.status_code in (200, 201):
            pid = resp.json().get("id")
            if pid is not None:
                ids.append(pid)
        return resp

    yield _factory

    for pid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/places/{pid}")
        except Exception:
            pass


@pytest.fixture
def created_camera(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/cameras", json=payload)
        if resp.status_code in (200, 201):
            cid = resp.json().get("id")
            if cid is not None:
                ids.append(cid)
        return resp

    yield _factory

    for cid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/cameras/{cid}")
        except Exception:
            pass


@pytest.fixture
def created_user(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/users", json=payload)
        if resp.status_code in (200, 201):
            uid = resp.json().get("id")
            if uid is not None:
                ids.append(uid)
        return resp

    yield _factory

    for uid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/users/{uid}")
        except Exception:
            pass


@pytest.fixture
def created_videowall(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/videowalls", json=payload)
        if resp.status_code in (200, 201):
            vid = resp.json().get("id")
            if vid is not None:
                ids.append(vid)
        return resp

    yield _factory

    for vid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/videowalls/{vid}")
        except Exception:
            pass


@pytest.fixture
def created_webhook(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/webhooks", json=payload)
        if resp.status_code in (200, 201):
            wid = resp.json().get("id")
            if wid is not None:
                ids.append(wid)
        return resp

    yield _factory

    for wid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/webhooks/{wid}")
        except Exception:
            pass


@pytest.fixture
def created_facelist(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/facelists", json=payload)
        if resp.status_code in (200, 201):
            fid = resp.json().get("id")
            if fid is not None:
                ids.append(fid)
        return resp

    yield _factory

    for fid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/facelists/{fid}")
        except Exception:
            pass


@pytest.fixture
def created_platelist(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/platelists", json=payload)
        if resp.status_code in (200, 201):
            pid = resp.json().get("id")
            if pid is not None:
                ids.append(pid)
        return resp

    yield _factory

    for pid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/platelists/{pid}")
        except Exception:
            pass


@pytest.fixture
def created_face(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/faces", json=payload)
        if resp.status_code in (200, 201):
            fid = resp.json().get("id")
            if fid is not None:
                ids.append(fid)
        return resp

    yield _factory

    for fid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/faces/{fid}")
        except Exception:
            pass


@pytest.fixture
def created_plate(api_client):
    ids: list[int] = []

    def _factory(payload: dict):
        resp = api_client.post("/api/v1/plates", json=payload)
        if resp.status_code in (200, 201):
            pid = resp.json().get("id")
            if pid is not None:
                ids.append(pid)
        return resp

    yield _factory

    for pid in reversed(ids):
        try:
            api_client.delete(f"/api/v1/plates/{pid}")
        except Exception:
            pass


