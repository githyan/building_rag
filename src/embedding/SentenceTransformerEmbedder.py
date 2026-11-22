from BaseEmbedder import BaseEmbedder


class SentenceTransformerEmbedder(BaseEmbedder):

    def __init__(
        self,
        model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
        batch_size: int = 32,
    ) -> None:
        self.model_name = model_name
        self.batch_size = batch_size
        self._model = None

    def _get_model(self) -> str | None:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)

        return self._model

    @property
    def dimension(self) -> int:
        return self._get_model().get_embedding_dimension()

    def embed_document(self, texts: list[str | Document]) -> list[list[float]]:

        return (
            []
            if not texts
            else self._get_model()
            .encode_document(
                texts,
                batch_size=self.batch_size,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            .tolist()
        )

    def embed_query(self, text: str | Document) -> list[float]:
        return self._get_model().encode_query(text)
