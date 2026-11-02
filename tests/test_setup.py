"""Testes de inicialização do projeto e configuração."""

import emporio_ozzy
from emporio_ozzy.config import Settings, get_settings


def test_package_import():
    """Valida se o pacote raiz pode ser importado e possui versão definida."""
    assert hasattr(emporio_ozzy, "__version__")
    assert emporio_ozzy.__version__ == "0.1.0"


def test_settings_defaults():
    """Valida se as configurações padrões são carregadas corretamente de forma agnóstica a OS."""
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.groq_model in ["llama-3.3-70b-versatile", "openai/gpt-oss-120b"]
    assert settings.db_path.as_posix() == "data/emporio.db"
    assert settings.chroma_path.as_posix() == "data/chroma"
