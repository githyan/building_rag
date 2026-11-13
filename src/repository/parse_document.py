import os
from psycopg2 import connect
from dotenv import load_dotenv

from src.document_processing.files import load_documents
from src.repository.interface import abstractRepository
from src.repository.SQLInjection import SQL_Injection
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

load_dotenv()


class ParsingDocument:
    def __init__(self, data) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", ", ", " ", ""],
        )

    def generate_chunk(self, data: list[Document]) -> list[Document]:
        text_split = self.text_splitter.split_documents(data)
        postgresql = SQL_Injection(
            os.getenv("DB_NAME"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
        )

        client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
        postgresql.sql_table_init()
        for idx, chunk in enumerate(text_split):
            response = client.models.embed_content(
                model=os.getenv("EMBEDDINGS_MODEL")
                contents=chunk.page_content,
            )
            embeddings = response.embeddings[0].values
            postgresql.create_chunks(
                idx,
                chunk.page_content,
                chunk.metadata["source"],
                chunk.metadata["filename"],
                embeddings,
            )
