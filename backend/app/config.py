from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file='.env')

    SECRET_KEY: str
    ALGORITHM: str
    MODEL_PATH: str

settings = Settings()
