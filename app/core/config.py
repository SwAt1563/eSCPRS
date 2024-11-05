from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os





class Settings(BaseSettings):
    FASTAPI_ENV: str = "production"
    MONGODB_PORT: int = 27017
    MONGODB_HOST: str = "mongodb"
    MONGODB_USER: str 
    MONGODB_PASSWORD: str 

    # Dynamically set the environment file based on FASTAPI_ENV: this will override the upper env
    model_config = SettingsConfigDict(
        env_file=".env.dev" if os.getenv("FASTAPI_ENV", "development") == "development" else ".env.prod" 
    )


# @lru_cache
# def get_settings():
#     return Settings()


# create just one instance of the settings when called the first time
settings = Settings()