import os
import pathlib
from pathlib import Path
import pypdf
import re
from langchain_core.documents import Document
from dataclasses import dataclass, field
from pypdf.errors import PdfReadError


@dataclass
class data:
    path: Path | None = None
    EXTENSION: set[str] = field(default_factory=lambda: {".md", ".txt"})
    documents: list[Document] = field(default_factory=list)

    def resolve(self, file_path: str | Path) -> Path:
        path = Path(file_path)
        candidates = [path] if path.is_absolute() else [path, self.path / path]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        tried = ", ".join(str(c.resolve()) for c in candidates)
        raise FileNotFoundError(
            f"{self.EXTENSION} tidak ditemukan. Sudah dicoba: {tried}"
        )


class DataLoader(data):

    def load_pdf_pages(self, file_path: str | Path) -> list[Document]:
        import logging

        logger = logging.getLogger(__name__)
        path = self.resolve(file_path)

        def _is_valid_pdf(path: Path) -> bool:
            with path.open("rb") as f:
                return f.read(1024).lstrip().startswith(b"%PDF-")

        if not _is_valid_pdf(path):
            logger.warning("Bukan PDF valid (header salah), dilewati: %s", path)
            return []

        try:
            reader = pypdf.PdfReader(path)
            return [
                Document(
                    page_content=page.extract_text() or "",
                    metadata={
                        "source": (
                            str(path.relative_to(self.path))
                            if path.is_relative_to(self.path)
                            else str(path)
                        ),
                        "filename": self.path.name,
                        "page": i + 1,
                    },
                )
                for i, page in enumerate(reader.pages)
            ]
        except PdfReadError as e:
            logger.waring("Gagal membaca %s: %s", path, e)
            return []

    def load_markdown_text(self, files: list[Path]) -> list[Document]:
        import logging

        logger = logging.getLogger(__name__)

        for f in files:
            try:
                text = f.read_text(encoding="UTF-8")
            except (UnicodeDecodeError, PermissionError) as error:
                logger.warning("gagal memuat: %s pada file %s", error, f)
                continue
            self.documents.append(
                Document(
                    page_content=text,
                    metadata={"source": str(f), "filename": self.path.name},
                )
            )

        return self.documents

    @property
    def extract_text(self) -> list[Document]:

        files: list[Path] = sorted(
            p
            for p in self.path.rglob("*")
            if p.is_file() and p.suffix.lower() in self.EXTENSION
        )
        for file in files:
            if file.name.endswith(".md") or file.name.endswith(".txt"):
                self.load_markdown_text(files)
            elif file.name.endswith(".pdf"):
                self.documents.extend(self.load_pdf_pages(file_path=file))

        return self.documents
