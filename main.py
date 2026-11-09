from os import get_exec_path
from pathlib import Path
from src.repository.parse_document import ParsingDocument
from src.repository.interface import abstractRepository
from src.repository.SQLInjection import SQL_Injection
from src.loading_chunks import load_dataset
import pandas as pd

from src.document_processing.files import load_documents
from src.document_processing.parse import parse_document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def main():
    print("Hello from workspaces!")
    load_df = load_documents(Path("dataset/dummy_md"), "*.md")
    df_extract = load_df.extract_documents()
    parse_docs = ParsingDocument(df_extract)
    get_parse = parse_docs.generate_chunk(df_extract)
    print(get_parse)


if __name__ == "__main__":
    main()
