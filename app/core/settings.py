from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGODB_URL: str

    MONGODB_DATABASE: str = 'clinical_control_db'
    MONGODB_USERS_COLLECTION: str = 'users'

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )


settings = Settings()
