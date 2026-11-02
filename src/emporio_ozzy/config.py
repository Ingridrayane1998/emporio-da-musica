from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação Ozzy carregadas de variáveis de ambiente ou .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Groq API
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Caminhos de dados
    db_path: Path = Path("data/emporio.db")
    chroma_path: Path = Path("data/chroma")
    embedding_model: str = "all-MiniLM-L6-v2"

    # Servidor API
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Retorna instância única (em cache) das configurações."""
    return Settings()

