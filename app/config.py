from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    proxy_api_key: str
    proxy_api_base_url: str = "https://api.proxyapi.ru/openai/v1"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2
    database_url: str = "sqlite:///./data/smart_support.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
