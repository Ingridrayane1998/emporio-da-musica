"""Módulo de recuperação semântica (Retriever) do RAG no ChromaDB."""

from pathlib import Path
from typing import Any, Optional

import chromadb

from emporio_ozzy.config import get_settings
from emporio_ozzy.rag.embeddings import get_embedding_function


def get_chroma_collection(
    chroma_dir: Optional[Path] = None, collection_name: str = "politicas_emporio"
):
    """Conecta ao ChromaDB persistente e retorna a coleção de políticas."""
    if chroma_dir is None:
        settings = get_settings()
        chroma_dir = settings.chroma_path

    embedding_fn = get_embedding_function(chroma_dir)
    client = chromadb.PersistentClient(path=str(chroma_dir))
    return client.get_collection(name=collection_name, embedding_function=embedding_fn)


def buscar_politicas(
    query: str,
    k: int = 4,
    score_threshold: float = 0.04,
    chroma_dir: Optional[Path] = None,
) -> list[dict[str, Any]]:
    """Busca trechos semânticos nas políticas da loja no ChromaDB."""
    collection = get_chroma_collection(chroma_dir)

    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    matched_chunks = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        # No espaço cosine do ChromaDB: distance = 1 - similarity
        similarity = round(max(0.0, 1.0 - float(dist)), 4)
        if similarity >= score_threshold:
            matched_chunks.append(
                {
                    "text": doc,
                    "page": meta.get("page", 1),
                    "section": meta.get("section", "Geral"),
                    "source": meta.get("source", "politicas_da_loja.pdf"),
                    "similarity": similarity,
                }
            )

    return matched_chunks


def formatar_contexto_politicas(chunks: list[dict[str, Any]]) -> str:
    """Formata os trechos recuperados em texto claro para alimentar o system prompt do Ozzy."""
    if not chunks:
        return "Nenhuma política específica encontrada para esta dúvida."

    formatted_sections = []
    for idx, c in enumerate(chunks, start=1):
        formatted_sections.append(
            f"[Trecho {idx} - {c['section']}]:\n{c['text']}"
        )

    return "\n\n".join(formatted_sections)

