from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )
    # Database url
    DATABASE_URL: str

    # Secret key
    SECRET_KEY: str


settings = Settings()
