"""Orquestrador principal do agente Ozzy via API do Groq com function calling."""

import json
import logging
from typing import Any, Optional

from groq import Groq

from emporio_ozzy.agent.guardrails import classify_message
from emporio_ozzy.agent.prompts import (
    OUT_OF_SCOPE_MESSAGE,
    SYSTEM_PROMPT,
    VERIFICATION_REQUIRED_MESSAGE,
)
from emporio_ozzy.config import get_settings
from emporio_ozzy.rag.retriever import buscar_politicas, formatar_contexto_politicas
from emporio_ozzy.tools import ALL_TOOLS
from emporio_ozzy.tools.schemas import TOOLS_DEFINITIONS

logger = logging.getLogger(__name__)

# Maximos de iteracoes do loop de tool calls por turno
MAX_TOOL_ITERATIONS = 5

# Ferramentas que exigem cliente verificado
_PROTECTED_TOOLS = {"consultar_pedido", "historico_pedidos"}


class OzzyAgent:
    """Agente Ozzy: orquestra LLM (Groq), tools SQL, RAG e guardrails."""

    def __init__(self) -> None:
        settings = get_settings()
        self._client = Groq(api_key=settings.groq_api_key)
        self._model = settings.groq_model
        # Memoria de curto prazo por sessao: {session_id: list[messages]}
        self._sessions: dict[str, list[dict[str, Any]]] = {}
        # Registro de clientes verificados: {session_id: customer_id}
        self._verified_customers: dict[str, int] = {}

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------

    def chat(self, message: str, session_id: str = "default") -> dict[str, Any]:
        """Processa uma mensagem do usuario e retorna a resposta do Ozzy.

        Returns:
            dict com chaves: reply (str), handoff (bool), ticket_id (str | None)
        """
        # 1. Guardrails pre-LLM
        flags = classify_message(message)

        if flags["injection"]:
            return self._build_reply(
                "Hmm, nao consigo processar esse tipo de solicitacao. "
                "Posso te ajudar com produtos, politicas ou seu pedido! 🎵"
            )

        if flags["out_of_scope"]:
            return self._build_reply(OUT_OF_SCOPE_MESSAGE)

        # 2. Adiciona mensagem do usuario ao historico da sessao
        history = self._get_history(session_id)
        history.append({"role": "user", "content": message})

        # 3. Loop de orquestracao: LLM → tool calls → LLM
        reply, handoff, ticket_id = self._orchestrate(history, session_id, flags)

        # 4. Salva resposta no historico
        history.append({"role": "assistant", "content": reply})
        self._sessions[session_id] = history[-20:]  # mantém últimas 20 mensagens

        return self._build_reply(reply, handoff=handoff, ticket_id=ticket_id)

    def reset_session(self, session_id: str) -> None:
        """Limpa o historico de uma sessao."""
        self._sessions.pop(session_id, None)
        self._verified_customers.pop(session_id, None)

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    def _get_history(self, session_id: str) -> list[dict[str, Any]]:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        return self._sessions[session_id]

    def _orchestrate(
        self,
        history: list[dict[str, Any]],
        session_id: str,
        flags: dict,
    ) -> tuple[str, bool, Optional[str]]:
        """Loop principal: chama o LLM, executa tools e retorna (reply, handoff, ticket_id)."""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        handoff = False
        ticket_id = None

        for _ in range(MAX_TOOL_ITERATIONS):
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=TOOLS_DEFINITIONS,
                tool_choice="auto",
                temperature=0.3,
                max_tokens=1024,
            )

            choice = response.choices[0]
            msg = choice.message

            # Se o LLM gerou texto final sem tool call, encerra
            if choice.finish_reason == "stop" or not msg.tool_calls:
                reply = msg.content or ""
                # Guardrail pos-LLM: empatia forcada se insatisfeito sem handoff
                if flags.get("dissatisfied") and not handoff:
                    reply = self._inject_empathy(reply)
                return reply, handoff, ticket_id

            # Processa tool calls
            messages.append(msg)  # adiciona mensagem do assistente com tool_calls

            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                raw_args = tool_call.function.arguments or "{}"

                try:
                    args = json.loads(raw_args)
                except json.JSONDecodeError:
                    args = {}

                tool_result = self._execute_tool(
                    tool_name, args, session_id, flags
                )

                # Detecta handoff
                if tool_name == "acionar_atendente":
                    handoff = True
                    try:
                        result_data = json.loads(tool_result)
                        ticket_id = result_data.get("ticket_id")
                    except Exception:
                        pass

                # Detecta verificacao de cliente
                if tool_name == "verificar_cliente":
                    try:
                        result_data = json.loads(tool_result)
                        if result_data.get("verificado"):
                            self._verified_customers[session_id] = result_data["customer_id"]
                    except Exception:
                        pass

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    }
                )

        # Fallback se excedeu iteracoes
        return (
            "Desculpe, tive um problema ao processar sua solicitacao. "
            "Posso acionar um atendente para te ajudar?",
            handoff,
            ticket_id,
        )

    def _execute_tool(
        self,
        tool_name: str,
        args: dict[str, Any],
        session_id: str,
        flags: dict,
    ) -> str:
        """Executa a ferramenta solicitada com validacoes de seguranca."""

        # Protecao: ferramentas de pedido exigem verificacao previa
        if tool_name in _PROTECTED_TOOLS:
            if session_id not in self._verified_customers:
                return json.dumps(
                    {
                        "erro": True,
                        "mensagem": VERIFICATION_REQUIRED_MESSAGE,
                    },
                    ensure_ascii=False,
                )
            # Injeta customer_id verificado no historico_pedidos
            if tool_name == "historico_pedidos" and "cliente_id" not in args:
                args["cliente_id"] = self._verified_customers[session_id]

        # Tool especial: buscar_politicas usa RAG diretamente
        if tool_name == "buscar_politicas":
            return self._run_rag_tool(args)

        # Demais tools no mapa ALL_TOOLS
        fn = ALL_TOOLS.get(tool_name)
        if fn is None:
            return json.dumps(
                {"erro": True, "mensagem": f"Ferramenta '{tool_name}' nao reconhecida."},
                ensure_ascii=False,
            )

        try:
            return fn(**args)
        except Exception as exc:
            logger.exception("Erro ao executar ferramenta %s: %s", tool_name, exc)
            return json.dumps(
                {"erro": True, "mensagem": "Erro interno ao executar a ferramenta."},
                ensure_ascii=False,
            )

    def _run_rag_tool(self, args: dict[str, Any]) -> str:
        """Executa busca RAG e retorna contexto formatado em JSON."""
        pergunta = args.get("pergunta", "")
        k = int(args.get("k", 4))
        try:
            chunks = buscar_politicas(pergunta, k=k)
            context = formatar_contexto_politicas(chunks)
            return json.dumps(
                {"encontrado": bool(chunks), "contexto": context},
                ensure_ascii=False,
            )
        except Exception as exc:
            logger.exception("Erro no RAG: %s", exc)
            return json.dumps(
                {"encontrado": False, "contexto": "Nao foi possivel consultar as politicas."},
                ensure_ascii=False,
            )

    @staticmethod
    def _inject_empathy(reply: str) -> str:
        """Prefixa empatia na resposta quando o cliente esta insatisfeito."""
        if not reply.startswith(("Entendo", "Sinto muito", "Lamento", "Compreendo")):
            return "Entendo sua frustracao e sinto muito por isso. " + reply
        return reply

    @staticmethod
    def _build_reply(
        reply: str, handoff: bool = False, ticket_id: Optional[str] = None
    ) -> dict[str, Any]:
        return {
            "reply": reply,
            "handoff": handoff,
            "ticket_id": ticket_id,
        }


# Instancia singleton do agente (reutilizada entre requests)
_agent_instance: Optional[OzzyAgent] = None


def get_agent() -> OzzyAgent:
    """Retorna a instancia singleton do OzzyAgent."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = OzzyAgent()
    return _agent_instance
