"""Ponto de entrada unificado das ferramentas do Ozzy."""

from emporio_ozzy.tools.catalog import CATALOG_TOOL_MAP
from emporio_ozzy.tools.orders import ORDERS_TOOL_MAP
from emporio_ozzy.tools.support import SUPPORT_TOOL_MAP

# Mapa global de todas as ferramentas disponíveis para o orquestrador
ALL_TOOLS: dict = {
    **CATALOG_TOOL_MAP,
    **ORDERS_TOOL_MAP,
    **SUPPORT_TOOL_MAP,
}

__all__ = ["ALL_TOOLS"]
