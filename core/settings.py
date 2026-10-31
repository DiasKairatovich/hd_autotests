from __future__ import annotations
from pathlib import Path
import re
import tomllib
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
import os
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_TOML = BASE_DIR / "configs" / "settings.toml"


class StreamNode(BaseModel):
    #Streamserver-нода: uuid — идентификатор в etcd (`/streamservers/<uuid>/...`),
    uuid: str
    ssh_host: str


class Settings(BaseSettings):
    env: str
    api_base_url: str
    openapi_path: str | None = "configs/openapi.json"
    openapi_url: str | None = None
    api_token: str | None = None
    token_type: str | None = "bearer"
    refresh_token: str | None = None
    request_timeout_s: float = 40.0

    username: str | None = None
    password: str | None = None

    ui_base_url: str | None = None

    etcd_host: str | None = None
    etcd_port: int = 2379

    rtsp_base_url: str | None = None
    dahua_source: str | None = None
    hikvision_source: str | None = None
    capacitygroup_token: str = "0000000000000000"
    scheduler_group: str = "default"
    group_id: int | None = None
    organization_id: int | None = 1
    kafka_brokers: list[str] = []
    cassandra_host: str | list[str] | None = None
    cassandra_port: int = 9042
    cassandra_user: str | None = None
    cassandra_password: str | None = None

    psql_host: str | None = None
    psql_user: str | None = None
    psql_password: str | None = None

    clickhouse_host: str | None = None
    clickhouse_port: int = 8123
    clickhouse_user: str | None = "teye"
    clickhouse_password: str | None = None

    vicmetrics_url: str | None = None

    redis_host: str | None = None
    redis_port: int = 6380
    redis_user: str | None = None
    redis_password: str | None = None

    qdrant_host: str | None = None
    qdrant_port: int = 6333
    qdrant_api_key: str | None = None

    seaweed_host: str | None = None
    mock_server_url: str | None = None

    nanny_host: str | None = None
    streamserver_nodes: dict[str, StreamNode] = {}

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

    def auth_header(self, token: str | None = None) -> dict[str, str]:
        """
        Заголовки к API: Accept + Authorization из текущего токена.
        """
        token = token or self.api_token
        if not token:
            raise RuntimeError(
                "api_token не задан — сначала получите токен (core.fixtures.auth)"
            )
        token_type = (self.token_type or "bearer").capitalize()
        return {"Accept": "application/json", "Authorization": f"{token_type} {token}"}

def _flat_stream_nodes(raw: dict) -> dict[str, StreamNode]:
    """
    Плоские ключи env-блока `<имя>_uuid` / `<имя>_ssh_host` — в словарь нод
    здесь пары собираются в `streamserver_nodes` для тестов
    """
    pair = re.compile(r"^(?P<name>\w+)_uuid$")
    nodes: dict[str, StreamNode] = {}
    for key, value in raw.items():
        match = pair.match(key)
        if not match:
            continue
        ssh_host = raw.get(f"{match.group('name')}_ssh_host")
        if ssh_host:
            nodes[match.group("name")] = StreamNode(uuid=value, ssh_host=ssh_host)
    return nodes


def load_settings(env: str, toml_path: Path = DEFAULT_TOML) -> Settings:
    if not env:
        env = "dev"

    with toml_path.open("rb") as f:
        data = tomllib.load(f)
    raw = (data.get("envs") or {}).get(env) or {}
    
    env_vars = dotenv_values(".env")
    env_upper = env.upper()

    for field_name in Settings.model_fields.keys():
        if field_name == "env":
            continue

        env_key = field_name.upper()
        prefixed_key = f"{env_upper}_{env_key}"

        val = os.getenv(prefixed_key, env_vars.get(prefixed_key))
        if val is not None:
            raw[field_name] = val
    
    raw["streamserver_nodes"] = _flat_stream_nodes(raw)

    return Settings(env=env, **raw)
