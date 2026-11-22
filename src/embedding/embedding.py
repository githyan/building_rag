from BaseEmbedder import BaseEmbedder
import numpy as np
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Menghitung kemiripan dua vector: 1 = mirip, 0 = tidak memiliki hubungan
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a)) or 0.0
    norm_b = math.sqrt(sum(y * y for y in b)) or 0.0

    return dot / (norm_a * norm_b)


def rank_document(
    embedder: BaseEmbedder, query: str, documents: list[str]
) -> list[tuple[float, str]]:
    """
    Mengurutkan Dokumen dari yang paling mirip dengan query.
    Fungsi ini menerima argument: BaseEmbedder, semua embedder diterima
    """
    doc_vectors = embedder.embed_document(documents)
    query_vector = embedder.embed_query(query)
    print(f"dimensi embedding dari {embedder.__class__.__name__}: {embedder.dimension}")
    scored = [
        (cosine_similarity(query_vector, vec), doc)
        for vec, doc in zip(doc_vectors, documents)
    ]
    return sorted(scored, key=lambda item: item[0], reverse=True)
