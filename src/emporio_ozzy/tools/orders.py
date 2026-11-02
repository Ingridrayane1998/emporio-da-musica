"""Ferramentas de pedidos e clientes: verificação, consulta e histórico."""

import json
from typing import Any

from emporio_ozzy.db.queries import get_customer_orders, get_order_details, verify_customer
from emporio_ozzy.db.session import get_session


def verificar_cliente(email_ou_telefone: str, numero_pedido: int) -> str:
    """Verifica identidade do cliente e retorna token de sessão em JSON."""
    with get_session() as db:
        result = verify_customer(db, email_or_phone=email_ou_telefone, order_id=numero_pedido)

    if not result:
        return json.dumps(
            {
                "verificado": False,
                "mensagem": (
                    "Não foi possível verificar o cliente. "
                    "Confira o e-mail/telefone e o número do pedido."
                ),
            },
            ensure_ascii=False,
        )

    return json.dumps(
        {
            "verificado": True,
            "customer_id": result["customer_id"],
            "nome": result["name"],
            "order_id": result["order_id"],
        },
        ensure_ascii=False,
    )


def consultar_pedido(numero_pedido: int) -> str:
    """Retorna detalhes de um pedido por ID em JSON."""
    with get_session() as db:
        detail = get_order_details(db, order_id=numero_pedido)

    if not detail:
        return json.dumps(
            {"encontrado": False, "mensagem": f"Pedido #{numero_pedido} não encontrado."},
            ensure_ascii=False,
        )

    return json.dumps({"encontrado": True, "pedido": detail}, ensure_ascii=False)


def historico_pedidos(cliente_id: int) -> str:
    """Lista histórico de pedidos de um cliente autenticado em JSON."""
    with get_session() as db:
        orders = get_customer_orders(db, customer_id=cliente_id)

    if not orders:
        return json.dumps(
            {"encontrado": False, "mensagem": "Nenhum pedido encontrado para este cliente."},
            ensure_ascii=False,
        )

    return json.dumps(
        {"encontrado": True, "total": len(orders), "pedidos": orders}, ensure_ascii=False
    )


# ---------------------------------------------------------------------------
# Mapa de dispatch para chamadas do LLM
# ---------------------------------------------------------------------------

ORDERS_TOOL_MAP: dict[str, Any] = {
    "verificar_cliente": verificar_cliente,
    "consultar_pedido": consultar_pedido,
    "historico_pedidos": historico_pedidos,
}

