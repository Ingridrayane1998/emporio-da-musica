"""Testes automatizados do pipeline RAG e avaliação de Hit Rate."""

from pathlib import Path

import yaml

from emporio_ozzy.rag.ingest_pdf import extract_and_chunk_pdf
from emporio_ozzy.rag.retriever import buscar_politicas, formatar_contexto_politicas


def test_pdf_extraction_and_chunking():
    """Valida a extração e segmentação de chunks semânticos do PDF."""
    pdf_path = Path("data/raw/politicas_da_loja.pdf")
    chunks = extract_and_chunk_pdf(pdf_path)
    assert len(chunks) >= 20
    for c in chunks:
        assert "chunk_id" in c
        assert "text" in c
        assert len(c["text"]) > 20
        assert 1 <= c["page"] <= 8
        assert "section" in c


def test_buscar_politicas_structure():
    """Valida a estrutura dos resultados retornados pelo retriever."""
    results = buscar_politicas("Qual o prazo de devolução por arrependimento?", k=3)
    assert len(results) > 0
    first = results[0]
    assert "text" in first
    assert "page" in first
    assert "section" in first
    assert "similarity" in first
    assert first["similarity"] > 0.0

    context = formatar_contexto_politicas(results)
    assert len(context) > 50
    assert "[Trecho" in context


def test_rag_evaluation_hit_rate():
    """Mede a taxa de acerto (Hit Rate >= 85%) sobre o conjunto de 16 perguntas de avaliação."""
    eval_file = Path("tests/rag_eval.yaml")
    with open(eval_file, "r", encoding="utf-8") as f:
        eval_data = yaml.safe_load(f)

    total_queries = len(eval_data)
    hits = 0
    misses = []

    for item in eval_data:
        query = item["query"]
        expected_pages = set(item["expected_pages"])
        results = buscar_politicas(query, k=4)
        retrieved_pages = {r["page"] for r in results}

        # Considera Hit se alguma das páginas esperadas estiver no top-k recuperado
        if expected_pages.intersection(retrieved_pages):
            hits += 1
        else:
            misses.append(
                {
                    "id": item["id"],
                    "query": query,
                    "expected": list(expected_pages),
                    "retrieved": list(retrieved_pages),
                }
            )

    hit_rate = (hits / total_queries) * 100.0
    print(f"\nRAG Evaluation: {hits}/{total_queries} hits ({hit_rate:.1f}%)")
    if misses:
        print("Consultas não correspondidas:", misses)

    # Critério de aceite obrigatório do plano mestre: Hit rate >= 85%
    assert (
        hit_rate >= 85.0
    ), f"Hit rate de {hit_rate:.1f}% abaixo do limiar mínimo de 85% ({hits}/{total_queries})"

