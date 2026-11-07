import os
import pathlib
from pathlib import Path
import re
from typing_extensions import Doc
from langchain_core.documents import Document


class load_documents:

    def __init__(self, path: Path, ext: str) -> None:
        self.path: Path = path
        self.extension: str = ext
        self.datasets: list[Document] = []

        if not isinstance(self.path, Path):
            raise TypeError(f"path must be a {type(Path)}")

    def extract_documents(self, ext_tuple=(".txt", ".md", ".pdf")):

        data_frame: list[Document] = []
        if self.extension[1:] in ext_tuple:
            isi_dir = list(self.path.rglob(f"{self.extension}"))
            self.datasets.extend(
                Document(
                    page_content=" ".join(f.read_text(encoding="UTF-8").split()),
                    metadata={"source": str(f), "filename": self.path.name},
                )
                for f in isi_dir
            )

        else:
            raise ValueError("input the right files extension")

        return self.datasets
