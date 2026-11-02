from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from emporio_ozzy.config import get_settings

app = FastAPI(
    title="Empório da Música & Ozzy API",
    description="Backend para chat e atendimento inteligente do assistente Ozzy",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios estáticos e templates
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "web" / "static"
TEMPLATES_DIR = BASE_DIR / "web" / "templates"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    products: list = []
    handoff: dict | None = None


@app.get("/", response_class=FileResponse)
def serve_index():
    """Serve a interface principal de chat do Ozzy."""
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Interface template não encontrada")
    return FileResponse(index_file)


@app.get("/api/health")
def health_check():
    """Endpoint de checagem de saúde da aplicação."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app": "Emporio Ozzy",
        "model": settings.groq_model,
        "version": "0.1.0",
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Endpoint preliminar de chat (a ser conectado com Groq Agent nas etapas seguintes)."""
    user_msg = req.message.lower().strip()

    # Respostas preliminares para validação de UI
    if "promoção" in user_msg or "guitarra" in user_msg or "promocao" in user_msg:
        return ChatResponse(
            reply=(
                "Temos guitarras fantásticas afinadas com até 20% de desconto! "
                "Dá uma olhada nessa belezura:"
            ),
            products=[
                {
                    "id": "gtr-sunburst-59",
                    "name": "Gibson Les Paul Standard 50s Sunburst",
                    "brand": "Gibson USA",
                    "price": 18990.0,
                    "originalPrice": 23740.0,
                    "discountPercent": 20,
                    "image": "/static/images/electric_guitar_sunburst_1793632768094.jpg",
                    "audioToneType": "rock",
                }
            ],
        )

    if "troca" in user_msg or "devolução" in user_msg or "devolucao" in user_msg:
        return ChatResponse(
            reply=(
                "Conforme a nossa política de trocas, você tem até 7 dias corridos após o "
                "recebimento para solicitar a devolução por arrependimento, ou até 30 dias para "
                "trocas por defeito de fábrica em instrumentos!"
            ),
        )

    if "atendente" in user_msg or "humano" in user_msg:
        return ChatResponse(
            reply=(
                "Com certeza! Já estou chamando nosso especialista em luthieria e atendimento "
                "para cuidar do seu caso com prioridade:"
            ),
            handoff={
                "ticket_id": "#TK-9821",
                "motivo": "Solicitação direta de atendente humano",
                "prioridade": "Alta",
            },
        )

    return ChatResponse(
        reply=(
            f"Recebi sua mensagem sobre '{req.message}'! Estou afinando as ferramentas de "
            "busca na nossa base de dados para te trazer todos os detalhes."
        ),
    )
