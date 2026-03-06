from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FACE_API_ENDPOINT: str
    FACE_API_KEY: str
    STORAGE_ACCOUNT_NAME: str
    STORAGE_CONTAINER_NAME: str
    STORAGE_CONNECTION_STRING: str

    model_config = SettingsConfigDict(env_file="app/.env")

settings = Settings()