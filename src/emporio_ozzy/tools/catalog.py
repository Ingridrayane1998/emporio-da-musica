"""Ferramentas de catálogo: busca de produtos, detalhamento e promoções."""

import json
from typing import Any, Optional

from emporio_ozzy.db.queries import (
    get_product_detail,
    list_active_promotions,
    search_products,
)
from emporio_ozzy.db.session import get_session


def buscar_produtos(
    termo: Optional[str] = None,
    categoria: Optional[str] = None,
    preco_max: Optional[float] = None,
    apenas_em_estoque: bool = True,
) -> str:
    """Busca produtos no catálogo e retorna JSON com os resultados."""
    with get_session() as db:
        results = search_products(
            db,
            term=termo,
            category_name=categoria,
            max_price=preco_max,
            in_stock_only=apenas_em_estoque,
            limit=5,
        )

    if not results:
        return json.dumps(
            {"encontrado": False, "mensagem": "Nenhum produto encontrado para os critérios."},
            ensure_ascii=False,
        )

    return json.dumps({"encontrado": True, "produtos": results}, ensure_ascii=False)


def detalhar_produto(produto_id: int) -> str:
    """Retorna detalhes completos de um produto por ID em JSON."""
    with get_session() as db:
        detail = get_product_detail(db, product_id=produto_id)

    if not detail:
        return json.dumps(
            {"encontrado": False, "mensagem": f"Produto ID {produto_id} não encontrado."},
            ensure_ascii=False,
        )

    return json.dumps({"encontrado": True, "produto": detail}, ensure_ascii=False)


def listar_promocoes(categoria: Optional[str] = None) -> str:
    """Lista as promoções vigentes em JSON, com filtro opcional por categoria."""
    with get_session() as db:
        promos = list_active_promotions(db, category_name=categoria)

    if not promos:
        return json.dumps(
            {"encontrado": False, "mensagem": "Nenhuma promoção ativa no momento."},
            ensure_ascii=False,
        )

    return json.dumps(
        {"encontrado": True, "total": len(promos), "promocoes": promos}, ensure_ascii=False
    )


# ---------------------------------------------------------------------------
# Mapa de dispatch para chamadas do LLM
# ---------------------------------------------------------------------------

CATALOG_TOOL_MAP: dict[str, Any] = {
    "buscar_produtos": buscar_produtos,
    "detalhar_produto": detalhar_produto,
    "listar_promocoes": listar_promocoes,
}

