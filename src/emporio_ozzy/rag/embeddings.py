"""Módulo de geração de embeddings vetoriais para o ChromaDB."""

from pathlib import Path
from typing import List, Optional

import joblib
import numpy as np
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbeddingFunction(EmbeddingFunction[Documents]):
    """Função de embeddings semânticos para o ChromaDB baseada em TF-IDF densificado."""

    def __init__(self, vectorizer: Optional[TfidfVectorizer] = None) -> None:
        self.vectorizer = vectorizer

    def fit(self, documents: List[str]) -> "TfidfEmbeddingFunction":
        """Treina o vetorizador no corpus dos documentos."""
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            strip_accents=None,  # Preserva acentuação em português
            lowercase=True,
        )
        self.vectorizer.fit(documents)
        return self

    def __call__(self, input: Documents) -> Embeddings:
        """Gera os vetores de embedding para a lista de documentos/perguntas."""
        if self.vectorizer is None:
            # Fallback caso ainda não tenha sido ajustado
            return [[0.0] * 128 for _ in input]

        matrix = self.vectorizer.transform(input).toarray()
        # Normalização L2 para similaridade por cosseno
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        normalized = (matrix / norms).astype(float)
        return normalized.tolist()

    def save(self, file_path: Path) -> None:
        """Salva o modelo vetorizador em disco."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.vectorizer, file_path)

    @classmethod
    def load(cls, file_path: Path) -> "TfidfEmbeddingFunction":
        """Carrega o modelo vetorizador do disco."""
        if not file_path.exists():
            return cls()
        vec = joblib.load(file_path)
        return cls(vectorizer=vec)


def get_embedding_function(
    chroma_dir: Path, corpus: Optional[List[str]] = None
) -> TfidfEmbeddingFunction:
    """Retorna a função de embeddings, carregando do disco ou ajustando ao corpus fornecido."""
    model_file = chroma_dir / "vectorizer.joblib"
    if model_file.exists():
        return TfidfEmbeddingFunction.load(model_file)

    ef = TfidfEmbeddingFunction()
    if corpus:
        ef.fit(corpus)
        ef.save(model_file)
    return ef

