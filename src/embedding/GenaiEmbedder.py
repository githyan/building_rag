import math

from BaseEmbedder import BaseEmbedder
from dotenv import load_dotenv

import os

load_dotenv()


class GenaiGoogleEmbedder(BaseEmbedder):

    def __init__(
        self,
        model_name: str | None = None,
        dim: int = 768,
        batch_size: int = 32,
        client=None,
    ) -> None:

        self.model_name = model_name or os.getenv("EMBEDDING_MODEL")
        self._dim = dim
        self.batch_size = batch_size
        self.client = client

    def _getclient(self):
        if self.client is None:
            from google import genai

            self.client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

        return self.client

    def _embed(self, texts: list[str | Document], task_type: str) -> list[list[float]]:
        from google.genai import types

        vectors: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            result = self._getclient().models.embed_content(
                model=self.model_name,
                contents=batch,
                config=types.EmbedContentConfig(
                    output_dimensionality=self._dim, task_type=task_type
                ),
            )

            vectors.extend(self._normalize(list(e.values)) for e in result.embeddings)
        return vectors

    @staticmethod
    def _normalize(vector: list[float]) -> list[float]:
        norm = math.sqrt(sum(v * v for v in vector)) or 0.0
        return [v / norm for v in vector]

    @property
    def dimension(self) -> int:
        return self._dim

    def embed_query(self, text: str | Document) -> list[float]:
        return self._embed([text], task_type="RETRIEVAL_QUERY")[0]

    def embed_document(self, texts: list[str | Document]) -> list[list[float]]:
        return [] if not texts else self._embed(texts, task_type="RETRIEVAL_DOCUMENT")
