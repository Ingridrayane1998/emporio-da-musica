"""Módulo de extração, limpeza e chunking do PDF de políticas da loja."""

import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

# Mapeamento semântico das seções por página
PAGE_SECTIONS = {
    1: "Informações Gerais, Endereço e Contato",
    2: "1. Sobre a Empório da Música e Horários de Funcionamento",
    3: "3. Formas de Pagamento e Condições Comerciais",
    4: "4. Política de Trocas, Devoluções e Garantia",
    5: "5. Frete, Prazos de Entrega e Frete Grátis",
    6: "6. Promoções, Descontos e Cupons",
    7: "7. Padrões de Atendimento e Escalonamento Humano",
    8: "8. Privacidade, Segurança e LGPD",
}


def clean_page_text(raw_text: str) -> str:
    """Remove cabeçalhos repetitivos, normaliza quebras de linha e espaços."""
    # Remove repetições de cabeçalho comuns do PDF
    text = re.sub(
        r"Emp[oó]rio\s+da\s+M[uú]sica\s+Manual\s+de\s+Pol[ií]ticas\s+e\s+Procedimentos",
        "",
        raw_text,
        flags=re.IGNORECASE,
    )
    # Remove sequências de quebras de linha dentro de palavras ou linhas únicas
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    joined = " ".join(lines)
    # Normaliza espaços múltiplos
    return re.sub(r"\s+", " ", joined).strip()


def chunk_text(
    text: str, page_num: int, section_name: str, chunk_size: int = 600, overlap: int = 80
) -> list[dict[str, Any]]:
    """Divide o texto da página em chunks semânticos com sobreposição controlada."""
    chunks = []
    if len(text) <= chunk_size:
        chunks.append(
            {
                "chunk_id": f"p{page_num}_c1",
                "text": text,
                "page": page_num,
                "section": section_name,
                "source": "politicas_da_loja.pdf",
            }
        )
        return chunks

    start = 0
    chunk_idx = 1
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)

        # Se não for o final do texto, tenta quebrar em um ponto final ou espaço
        if end < text_len:
            last_period = text.rfind(". ", start, end)
            last_space = text.rfind(" ", start, end)
            if last_period != -1 and last_period > start + (chunk_size // 2):
                end = last_period + 1
            elif last_space != -1 and last_space > start + (chunk_size // 2):
                end = last_space

        chunk_content = text[start:end].strip()
        if chunk_content:
            chunks.append(
                {
                    "chunk_id": f"p{page_num}_c{chunk_idx}",
                    "text": chunk_content,
                    "page": page_num,
                    "section": section_name,
                    "source": "politicas_da_loja.pdf",
                }
            )
            chunk_idx += 1

        if end >= text_len:
            break

        start = end - overlap

    return chunks


def extract_and_chunk_pdf(pdf_path: Path) -> list[dict[str, Any]]:
    """Lê o PDF de políticas, limpa o texto e gera chunks com metadados estruturados."""
    reader = PdfReader(str(pdf_path))
    all_chunks = []

    for page_idx, page in enumerate(reader.pages):
        page_num = page_idx + 1
        raw_text = page.extract_text() or ""
        cleaned = clean_page_text(raw_text)
        section = PAGE_SECTIONS.get(page_num, f"Seção Página {page_num}")

        page_chunks = chunk_text(cleaned, page_num, section)
        all_chunks.extend(page_chunks)

    return all_chunks


if __name__ == "__main__":
    pdf_file = Path("data/raw/politicas_da_loja.pdf")
    chunks = extract_and_chunk_pdf(pdf_file)
    print(f"Total de chunks gerados: {len(chunks)}")
    for c in chunks[:3]:
        print(f"\nID: {c['chunk_id']} (Pág {c['page']} - {c['section']}):")
        print(f"Texto: {c['text'][:120]}...")

