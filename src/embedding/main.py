from SentenceTransformerEmbedder import SentenceTransformerEmbedder
from GenaiEmbedder import GenaiGoogleEmbedder
from embedding import rank_document

docs = [
    "Ibu kota Indonesia adalah Jakarta.",
    "Malang terkenal dengan apel dan wisata pegunungan.",
    "PostgreSQL bisa menyimpan dan mencari vektor lewat ekstensi pgvector.",
]
question = "Database apa yang bisa menyimpan vektor?"
# embedder = GenaiGoogleEmbedder(dim=3072)
embedder = SentenceTransformerEmbedder()

for score, doc in rank_document(embedder, question, docs):
    print(f"{score:.3f}|{doc}")
