"""Guardrails: deteccao de fora de escopo, insatisfacao e prompt injection."""

import re
import unicodedata


def _normalize_text(text: str) -> str:
    """Remove acentos e converte para minusculas para correspondencia resiliente."""
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# ---------------------------------------------------------------------------
# Palavras-chave de fora do escopo (topicos nao relacionados a loja)
# ---------------------------------------------------------------------------
_OUT_OF_SCOPE_PATTERNS = [
    r"\bpolitica\s+(partidaria|eleitoral|governo)\b",
    r"\beleic(ao|oes)\b",
    r"\bgoverno\b",
    r"\breceita(s)?\s+(culinaria|de\s+bolo|de\s+cozinha)\b",
    r"\bprogramacao\b",
    r"\bpython\b",
    r"\bjavascript\b",
    r"\bsql\b",
    r"\bfutebol\b",
    r"\btime\s+de\s+futebol\b",
    r"\bfilme(s)?\b",
    r"\bserie(s)?\b",
]

# ---------------------------------------------------------------------------
# Palavras-chave de insatisfacao / cliente irritado
# ---------------------------------------------------------------------------
_DISSATISFACTION_KEYWORDS = [
    "absurdo",
    "pessimo",
    "horrivel",
    "nunca mais",
    "inaceitavel",
    "reclamacao",
    "reclamar",
    "enganado",
    "mentira",
    "fraude",
    "roubado",
    "roubaram",
    "decepcionado",
    "decepcionante",
    "vergonha",
    "ridiculo",
    "inadmissivel",
    "prejuizo",
    "cancelar",
    "cancelamento",
    "reembolso",
    "furto",
]

# ---------------------------------------------------------------------------
# Padroes de prompt injection
# ---------------------------------------------------------------------------
_INJECTION_PATTERNS = [
    r"ignore\s+(as\s+)?(suas\s+)?(instrucoes|regras|prompt)",
    r"esqueca\s+(o\s+)?(que\s+)?(foi\s+)?dito",
    r"revele\s+(o\s+)?prompt",
    r"mostre\s+(o\s+)?(seu\s+)?prompt",
    r"execute\s+sql",
    r"select\s+\*\s+from",
    r"drop\s+table",
    r"system\s*:\s*",
    r"act\s+as\s+(a\s+)?(different|new)",
    r"jailbreak",
    r"dan\s+mode",
]


def is_out_of_scope(message: str) -> bool:
    """Retorna True se a mensagem claramente sai do escopo da loja."""
    text = _normalize_text(message)
    return any(re.search(p, text) for p in _OUT_OF_SCOPE_PATTERNS)


def is_dissatisfied(message: str) -> bool:
    """Retorna True se a mensagem indica cliente insatisfeito ou irritado."""
    text = _normalize_text(message)
    return any(kw in text for kw in _DISSATISFACTION_KEYWORDS)


def is_prompt_injection(message: str) -> bool:
    """Retorna True se a mensagem contem tentativa de prompt injection."""
    text = _normalize_text(message)
    return any(re.search(p, text) for p in _INJECTION_PATTERNS)


def classify_message(message: str) -> dict:
    """Classifica a mensagem do usuario em categorias de guardrail."""
    return {
        "out_of_scope": is_out_of_scope(message),
        "dissatisfied": is_dissatisfied(message),
        "injection": is_prompt_injection(message),
    }
