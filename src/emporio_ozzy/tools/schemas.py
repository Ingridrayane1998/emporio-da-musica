"""Schemas Pydantic e definições de function calling para as ferramentas do Ozzy."""

from typing import Any, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Schemas de entrada (validação das chamadas do LLM)
# ---------------------------------------------------------------------------


class BuscarPoliticasInput(BaseModel):
    """Parâmetros para busca semântica no PDF de políticas."""

    pergunta: str = Field(..., description="Pergunta ou assunto sobre políticas da loja.")
    k: int = Field(4, ge=1, le=8, description="Número de trechos a retornar.")


class BuscarProdutosInput(BaseModel):
    """Parâmetros para busca no catálogo de produtos."""

    termo: Optional[str] = Field(None, description="Palavra-chave para busca por nome/descrição.")
    categoria: Optional[str] = Field(None, description="Filtro por nome de categoria.")
    preco_max: Optional[float] = Field(None, description="Teto de preço em R$.")
    apenas_em_estoque: bool = Field(True, description="Se True, retorna só produtos em estoque.")


class DetalharProdutoInput(BaseModel):
    """Parâmetros para detalhar um produto específico."""

    produto_id: int = Field(..., description="ID numérico do produto.")


class ListarPromocoesInput(BaseModel):
    """Parâmetros para listar promoções vigentes."""

    categoria: Optional[str] = Field(None, description="Filtro opcional por categoria.")


class VerificarClienteInput(BaseModel):
    """Parâmetros para verificação de identidade do cliente."""

    email_ou_telefone: str = Field(
        ..., description="E-mail ou telefone do cliente para verificação."
    )
    numero_pedido: int = Field(..., description="Número (ID) do pedido a consultar.")


class ConsultarPedidoInput(BaseModel):
    """Parâmetros para consulta de pedido (exige cliente verificado)."""

    numero_pedido: int = Field(..., description="ID do pedido.")


class HistoricoPedidosInput(BaseModel):
    """Parâmetros para histórico de pedidos (exige cliente verificado)."""

    cliente_id: int = Field(..., description="ID do cliente autenticado.")


class AcionarAtendenteInput(BaseModel):
    """Parâmetros para acionar atendente humano e criar ticket."""

    motivo: str = Field(..., description="Descrição do motivo do acionamento.")
    prioridade: str = Field("Alta", description="Prioridade do ticket: Baixa, Média ou Alta.")
    resumo_conversa: Optional[str] = Field(
        None, description="Resumo da conversa até o momento."
    )


# ---------------------------------------------------------------------------
# Definições de tools para a API do Groq (function calling JSON)
# ---------------------------------------------------------------------------

TOOLS_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "buscar_politicas",
            "description": (
                "Busca informações sobre políticas da loja (trocas, devoluções, prazos, "
                "garantia, frete, pagamento, horários, contato) no banco vetorial. "
                "Use sempre que o cliente perguntar sobre regras, políticas ou informações "
                "institucionais da Empório da Música."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pergunta": {
                        "type": "string",
                        "description": "Pergunta ou assunto sobre políticas da loja.",
                    },
                    "k": {
                        "type": "integer",
                        "description": "Número de trechos a retornar (padrão: 4).",
                        "default": 4,
                    },
                },
                "required": ["pergunta"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_produtos",
            "description": (
                "Busca produtos no catálogo da loja por palavra-chave, categoria, "
                "faixa de preço e disponibilidade em estoque."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "termo": {
                        "type": "string",
                        "description": "Palavra-chave para busca por nome ou descrição.",
                    },
                    "categoria": {
                        "type": "string",
                        "description": "Filtro por categoria (ex: guitarras, teclados).",
                    },
                    "preco_max": {
                        "type": "number",
                        "description": "Preço máximo em R$.",
                    },
                    "apenas_em_estoque": {
                        "type": "boolean",
                        "description": "Se true, retorna apenas produtos em estoque.",
                        "default": True,
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "detalhar_produto",
            "description": (
                "Retorna detalhes completos de um produto: especificações técnicas, "
                "preço, estoque, promoções ativas. Use quando o cliente quiser saber "
                "mais sobre um produto específico já identificado."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "produto_id": {
                        "type": "integer",
                        "description": "ID numérico do produto.",
                    }
                },
                "required": ["produto_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_promocoes",
            "description": (
                "Lista as promoções e descontos vigentes na loja. "
                "Pode filtrar por categoria."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {
                        "type": "string",
                        "description": "Filtro por categoria (opcional).",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "verificar_cliente",
            "description": (
                "Verifica a identidade do cliente usando e-mail ou telefone junto ao "
                "número do pedido. OBRIGATÓRIO antes de qualquer consulta de pedido ou "
                "dados pessoais. Retorna token de sessão com customer_id se verificado."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "email_ou_telefone": {
                        "type": "string",
                        "description": "E-mail ou telefone do cliente.",
                    },
                    "numero_pedido": {
                        "type": "integer",
                        "description": "Número (ID) do pedido.",
                    },
                },
                "required": ["email_ou_telefone", "numero_pedido"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_pedido",
            "description": (
                "Retorna status, itens, valor total, código de rastreio e previsão de entrega "
                "de um pedido. Só pode ser chamado após verificar_cliente confirmar a identidade."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "numero_pedido": {
                        "type": "integer",
                        "description": "ID do pedido a consultar.",
                    }
                },
                "required": ["numero_pedido"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "historico_pedidos",
            "description": (
                "Lista os últimos pedidos de um cliente autenticado. "
                "Só pode ser chamado após verificar_cliente."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "cliente_id": {
                        "type": "integer",
                        "description": "ID do cliente autenticado.",
                    }
                },
                "required": ["cliente_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "acionar_atendente",
            "description": (
                "Aciona um atendente humano, cria ticket no sistema e notifica a equipe. "
                "Use quando: o cliente solicitar atendente, estiver insatisfeito e não "
                "resolver com as ferramentas, ou quando não houver informação suficiente "
                "para responder."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "motivo": {
                        "type": "string",
                        "description": "Motivo do acionamento.",
                    },
                    "prioridade": {
                        "type": "string",
                        "enum": ["Baixa", "Média", "Alta"],
                        "description": "Prioridade do atendimento.",
                        "default": "Alta",
                    },
                    "resumo_conversa": {
                        "type": "string",
                        "description": "Breve resumo da conversa até agora.",
                    },
                },
                "required": ["motivo"],
            },
        },
    },
]
