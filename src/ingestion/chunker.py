import os
from psycopg2 import connect
from dotenv import load_dotenv

from src.database.db import psql
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

load_dotenv()


class ParsingDocument:
    def __init__(self, data) -> None:
        self.client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", ", ", " ", ""],
        )
        self.postgresql = psql(
            os.getenv("DB_NAME"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
        )

    def generate_chunk(self, data: list[Document]) -> list[Document]:
        text_split = self.text_splitter.split_documents(data)

        self.postgresql.psql_connection()
        for idx, chunk in enumerate(text_split):
            response = self.client.models.embed_content(
                model=os.getenv("EMBEDDING_MODEL"), contents=chunk.page_content
            )
            embeddings = response.embeddings[0].values
            self.postgresql.create_chunks(
                idx,
                chunk.page_content,
                chunk.metadata["source"],
                chunk.metadata["filename"],
                embeddings,
            )

    def get_chunks(self, question):
        response = self.client.models.embed_content(
            model=os.getenv("EMBEDDING_MODEL"), contents=question
        )
        embedding = response.embeddings[0].values
        return self.postgresql.retrieve_chunks(embedding)
