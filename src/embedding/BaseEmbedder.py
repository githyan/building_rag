from __future__ import annotations

import hashlib
import math
from abc import ABC, abstractmethod
from langchain_core.documents import Document


class BaseEmbedder(ABC):

    @property
    @abstractmethod
    def dimension(self) -> int:
        pass

    @abstractmethod
    def embed_document(self, texts: list[str | Document]) -> list[list[float]]:
        pass

    def embed_query(self, text: str | Document) -> list[float]:
        return self.embed_document([text])[0]
