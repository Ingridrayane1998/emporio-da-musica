#!/usr/bin/env python3
"""
Script idempotente para criação e indexação do banco vetorial ChromaDB com as políticas da loja.
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao sys.path para import direto
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import chromadb  # noqa: E402

from emporio_ozzy.config import get_settings  # noqa: E402
from emporio_ozzy.rag.embeddings import get_embedding_function  # noqa: E402
from emporio_ozzy.rag.ingest_pdf import extract_and_chunk_pdf  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def build_vectorstore(pdf_path: Path, chroma_dir: Path) -> None:
    """Extrai os chunks do PDF e popula o ChromaDB de forma idempotente."""
    if not pdf_path.exists():
        print(f"[ERRO] Arquivo PDF não encontrado: {pdf_path}")
        sys.exit(1)

    print("=" * 60)
    print("Iniciando ingestão do PDF e indexação no ChromaDB...")
    print(f"Origem PDF:  {pdf_path.as_posix()}")
    print(f"Destino DB:  {chroma_dir.as_posix()}")
    print("=" * 60)

    # 1. Extração e Chunking
    chunks = extract_and_chunk_pdf(pdf_path)
    print(f"[OK] {len(chunks)} chunks semânticos gerados a partir do PDF.")

    # 2. Ajuste e salvamento do modelo de embeddings
    corpus = [c["text"] for c in chunks]
    embedding_fn = get_embedding_function(chroma_dir, corpus=corpus)
    print("[OK] Modelo de embeddings ajustado e calibrado com o corpus.")

    # 3. Inicialização do ChromaDB persistente
    chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_dir))

    collection_name = "politicas_emporio"
    # Idempotência: remove a coleção anterior se existir
    existing_collections = [col.name for col in client.list_collections()]
    if collection_name in existing_collections:
        client.delete_collection(name=collection_name)
        print(f"[INFO] Coleção anterior '{collection_name}' removida para reindexação.")

    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )

    # 4. Inserção no ChromaDB
    ids = [c["chunk_id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "page": c["page"],
            "section": c["section"],
            "source": c["source"],
        }
        for c in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"[SUCESSO] {len(ids)} documentos vetoriais indexados com sucesso no ChromaDB!")


if __name__ == "__main__":
    settings = get_settings()
    pdf = Path("data/raw/politicas_da_loja.pdf")
    build_vectorstore(pdf, settings.chroma_path)

