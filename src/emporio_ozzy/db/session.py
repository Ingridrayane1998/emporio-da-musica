"""Gerenciamento de conexao e sessao do banco de dados SQLite."""

from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from emporio_ozzy.config import get_settings


def get_engine(db_path: Path | str | None = None) -> Engine:
    """Cria a engine do SQLAlchemy para o SQLite local."""
    if db_path is None:
        settings = get_settings()
        db_path = settings.db_path

    path_obj = Path(db_path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    url = f"sqlite:///{path_obj.as_posix()}"
    return create_engine(
        url,
        connect_args={"check_same_thread": False},
        echo=False,
    )


def get_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    """Retorna uma fabrica de sessoes configurada para a engine."""
    if engine is None:
        engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Gerador de sessao para injecao de dependencia no FastAPI."""
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager de sessao para uso direto nas ferramentas do Ozzy."""
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
