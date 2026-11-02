#!/usr/bin/env python3
"""Script de execucao do servidor de desenvolvimento local para Emporio da Musica & Ozzy."""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Adiciona o diretorio src ao sys.path para import direto
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import uvicorn  # noqa: E402

from emporio_ozzy.config import get_settings  # noqa: E402


def main():
    settings = get_settings()
    print("=" * 60)
    print("Emporio da Musica & Ozzy - Servidor Local de Desenvolvimento")
    print(f"Acesse no navegador: http://{settings.host}:{settings.port}")
    print(f"Checagem de saude:   http://{settings.host}:{settings.port}/api/health")
    print("=" * 60)

    uvicorn.run(
        "emporio_ozzy.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
