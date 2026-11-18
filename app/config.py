from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    DISCORD_WEBHOOK_URL: str = ""

    LINKEDIN_ACCESS_TOKEN: str = ""
    LINKEDIN_AUTHOR_URN: str = ""
    LINKEDIN_API_VERSION: str = "202609"

    DEVTO_API_KEY: str = ""

    SLACK_WEBHOOK_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()