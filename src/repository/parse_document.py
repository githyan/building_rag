from psycopg2 import connect

from src.document_processing.files import load_documents
from src.repository.interface import abstractRepository
from src.repository.SQLInjection import SQL_Injection
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ParsingDocument:
    def __init__(self, data) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", ", ", " ", ""],
        )

    def generate_chunk(self, data: list[Document]) -> list[Document]:
        postgresql = SQL_Injection(
            "learn_from_dummy", "root", "root", "172.17.0.1", "5432"
        )

        postgresql.get_chunks()
        text_split = self.text_splitter.split_documents(data)
        postgresql.create_chunks(text_split)

        return data
