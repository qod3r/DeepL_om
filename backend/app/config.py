from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str 
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file='.env')

    SECRET_KEY: str
    ALGORITHM: str
    MODEL_PATH: str
    BROKER_URL: str

settings = Settings()
