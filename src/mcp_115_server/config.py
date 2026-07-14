from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, file_secret_settings

    p115_access_token: str | None = Field(default=None, alias="P115_ACCESS_TOKEN")
    p115_refresh_token: str | None = Field(default=None, alias="P115_REFRESH_TOKEN")

    p115_rate_limit: int = Field(default=1, alias="P115_RATE_LIMIT", ge=0)

    fastmcp_transport: str = Field(default="stdio", alias="FASTMCP_TRANSPORT")
    fastmcp_host: str = Field(default="127.0.0.1", alias="FASTMCP_HOST")
    fastmcp_port: int = Field(default=8000, alias="FASTMCP_PORT")
    fastmcp_path: str = Field(default="/mcp", alias="FASTMCP_PATH")
    fastmcp_log_level: str = Field(default="info", alias="FASTMCP_LOG_LEVEL")
    p115_debug_logging: bool = Field(default=True, alias="P115_DEBUG_LOGGING")
    p115_debug_log_file: str | None = Field(default="./logs/115-mcp-debug.log", alias="P115_DEBUG_LOG_FILE")

    @property
    def has_auth_configuration(self) -> bool:
        return bool(self.p115_refresh_token)

    @property
    def debug_log_file_path(self) -> Path | None:
        if not self.p115_debug_log_file:
            return None
        return Path(self.p115_debug_log_file).expanduser()
