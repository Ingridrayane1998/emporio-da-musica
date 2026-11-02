"""Backend FastAPI do Ozzy — endpoints de chat, sessao e health."""

import logging
import uuid
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from emporio_ozzy.agent.ozzy import get_agent
from emporio_ozzy.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Emporio da Musica & Ozzy API",
    description="Backend para chat e atendimento inteligente do assistente Ozzy",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — permite chamadas do front-end local
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Arquivos estaticos e templates
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "web" / "static"
TEMPLATES_DIR = BASE_DIR / "web" / "templates"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class SessionResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    products: list[dict[str, Any]] = []
    handoff: Optional[dict[str, Any]] = None
    session_id: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/", response_class=FileResponse)
def serve_index():
    """Serve a interface principal de chat do Ozzy."""
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Interface template nao encontrada")
    return FileResponse(index_file)


@app.get("/api/health")
def health_check():
    """Endpoint de checagem de saude da aplicacao."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app": "Emporio Ozzy",
        "model": settings.groq_model,
        "version": "1.0.0",
    }


@app.post("/api/session", response_model=SessionResponse)
def create_session():
    """Cria uma nova sessao de chat e retorna seu ID unico."""
    session_id = str(uuid.uuid4())
    return SessionResponse(session_id=session_id)


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Endpoint principal de chat — processa mensagem via agente Ozzy."""
    # Garante session_id
    session_id = req.session_id or str(uuid.uuid4())

    try:
        agent = get_agent()
        result = agent.chat(message=req.message, session_id=session_id)
    except Exception as exc:
        logger.exception("Erro no agente Ozzy: %s", exc)
        return ChatResponse(
            reply=(
                "Opa, tive uma pequena oscilacao na conexao com o palco! "
                "Pode repetir sua pergunta? 🎸"
            ),
            session_id=session_id,
        )

    # Monta handoff dict para o front-end se houver ticket
    handoff_data: Optional[dict[str, Any]] = None
    if result.get("handoff"):
        handoff_data = {
            "ticket_id": result.get("ticket_id", "#TK-????"),
            "motivo": "Atendente humano solicitado",
            "prioridade": "Alta",
        }

    return ChatResponse(
        reply=result["reply"],
        products=[],  # produtos inline via texto do Ozzy; extensao futura
        handoff=handoff_data,
        session_id=session_id,
    )


@app.delete("/api/session/{session_id}")
def reset_session(session_id: str):
    """Limpa o historico de uma sessao de chat."""
    agent = get_agent()
    agent.reset_session(session_id)
    return {"cleared": True, "session_id": session_id}
