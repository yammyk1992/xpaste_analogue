from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    postgres_user: str = "user"
    postgres_pass: str = "pass"
    db_host: str = "db"
    db_port: str = "1111"
    db_name: str = "name"
    secret_key: str = "secret"


settings = Settings()
