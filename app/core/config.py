from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os





class Settings(BaseSettings):
    FASTAPI_ENV: str = "development"
    FRONTEND_URL: str = "http://localhost:3000"

    MONGODB_PORT: int = 27017
    MONGODB_HOST: str = "mongodb" # This should match the service name in Docker Compose or the hostname of your mongodb service
    MONGODB_USER: str 
    MONGODB_PASSWORD: str 
    MONGODB_DATABASE: str

    # num_ctx=8192, num_predict=8000 -> means that just 192 tokens left for input
    # num_ctx=8192, num_predict=-1 -> means that 8192 tokens for (input + output)
    LLM_MODEL: str = "gemma2:2b" 
    LLM_MODEL_CTX: int = 2048
    LLM_MODEL_PREDICT: int = -1

    OLLAMA_HOST: str  # This should match the service name in Docker Compose or the hostname of your Ollama service
    OLLAMA_PORT: int 


    # Dynamically set the environment file based on FASTAPI_ENV: this will override the upper env
    model_config = SettingsConfigDict(
        env_file=".env.dev" if os.getenv("FASTAPI_ENV", "development") == "development" else ".env.prod" 
    )

    @property
    def OLLAMA_BASE_URL(self) -> str:
        return f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}"

    @property
    def MONGO_URL(self) -> str:
        return f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}/"


# @lru_cache
# def get_settings():
#     return Settings()


# create just one instance of the settings when called the first time
settings = Settings()