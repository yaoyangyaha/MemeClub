from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "123456"
    mysql_database: str = "meme_club"
    secret_key: str = "replace-this-with-a-long-random-string"
    access_token_expire_seconds: int = 31536000
    cookie_name: str = "meme_club_token"
    cookie_secure: bool = False
    frontend_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    frontend_origin: str | None = Field(default=None)

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )

    @property
    def cors_origins(self) -> list[str]:
        raw_value = self.frontend_origins
        if self.frontend_origin:
            raw_value = f"{raw_value},{self.frontend_origin}"
        return list(dict.fromkeys(origin.strip() for origin in raw_value.split(",") if origin.strip()))


settings = Settings()
