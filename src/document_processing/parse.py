import re
import string
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class parse_document:
    def __init__(self, datasets) -> None:
        self.datasets = datasets
        self.all_document_metadata: list[Document] = []

    def is_valid_hashtag(self, tag: str):
        HEADER_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
        return bool(re.match(HEADER_PATTERN, tag))

    def parse_markdown(self, chunk_source: str) -> list:

        current_content, section = [], []
        current_header = None

        # implementasi sebuah string processing untuk menghapus hashtag pada
        # sebuah teks header
        translator = str.maketrans("", "", string.punctuation)

        for i, text in enumerate(chunk_source.splitlines()):
            if self.is_valid_hashtag(text):
                if current_header is not None:
                    section.append(
                        {
                            "content_id": i,
                            "content": "\n".join(current_content),
                            "header": current_header.translate(translator),
                        }
                    )

                current_header = text
                current_content = []

            elif text.strip():
                current_content.append(text)

        if current_header is not None:
            section.append(
                {
                    "content_id": i,
                    "content": "\n".join(current_content),
                    "header": current_header.translate(translator),
                }
            )

        return section

    # chunking function untuk membuat chunks metadata
    def chunking(self, chunk_size: int = 100, chunk_overlap: int = 50):

        # Penerapan chunking dari langchain_core, ini lebih baik karena menerapkan pemotongan
        # setiap kata dari sequences berdasarkan pada makna semantic dokumen
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", ", ", " ", ""],
        )

        for data in self.datasets:
            source = data.metadata["source"]
            filename = data.metadata["filename"]

            # Ekstraksi chunks dari data page_content yang berisi dokumen Markdown
            semantic_chunks = splitter.split_text(data.page_content)
            parsed_chunk = map(self.parse_markdown, semantic_chunks)
            new_metadata: list[Document] = []
            for section in parsed_chunk:
                new_metadata.extend(filter(lambda x: x["content"].strip(), section))
                self.save_metadata(new_metadata, source, filename)

        return self.all_document_metadata

    def save_metadata(
        self, metadata_chunks: list[Document], src_metadata: str, file_metadata: str
    ):
        return self.all_document_metadata.extend(
            Document(
                page_content=document["content"],
                metadata={
                    "source": src_metadata,
                    "filename": file_metadata,
                    "chunk_id": document["content_id"],
                    "title": document["header"],
                },
            )
            for document in metadata_chunks
        )
