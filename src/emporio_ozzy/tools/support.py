"""Ferramentas de suporte: acionamento de atendente humano e criação de ticket."""

import json
from typing import Any, Optional

from emporio_ozzy.db.queries import create_ticket
from emporio_ozzy.db.session import get_session


def acionar_atendente(
    motivo: str,
    prioridade: str = "Alta",
    resumo_conversa: Optional[str] = None,
    customer_id: Optional[int] = None,
) -> str:
    """Cria ticket de atendimento humano no banco e retorna confirmação em JSON."""
    prioridade_valida = prioridade if prioridade in ("Baixa", "Média", "Alta") else "Alta"

    with get_session() as db:
        ticket = create_ticket(
            db,
            reason=motivo,
            priority=prioridade_valida,
            conversation_summary=resumo_conversa,
            customer_id=customer_id,
        )

    return json.dumps(
        {
            "acionado": True,
            "ticket_id": ticket["ticket_id"],
            "prioridade": ticket["priority"],
            "status": ticket["status"],
            "criado_em": ticket["created_at"],
            "mensagem": (
                "Atendente humano acionado com sucesso! "
                f"Seu ticket é {ticket['ticket_id']} — nossa equipe entrará em contato em breve."
            ),
        },
        ensure_ascii=False,
    )


# ---------------------------------------------------------------------------
# Mapa de dispatch para chamadas do LLM
# ---------------------------------------------------------------------------

SUPPORT_TOOL_MAP: dict[str, Any] = {
    "acionar_atendente": acionar_atendente,
}

