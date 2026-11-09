import os
import psycopg2 as psy
from pathlib import Path
from dotenv import load_dotenv

from src.repository.interface import abstractRepository
from langchain_core.documents import Document
from google import genai

load_dotenv()


class SQL_Injection(abstractRepository):

    def __init__(
        self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str
    ):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

        self.connect = psy.connect(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
        )
        self.curr = self.connect.cursor()
        self.auto_commit = self.connect.autocommit = True

    def retrieves_chunk(self):
        self.curr.execute("SELECT * FROM python.dbrag;")

    def connecting(self) -> bool:
        connection_state = True
        if self.curr and self.connect is None:
            connection_state = False
            self.curr.close()
            self.connect.close()

        return connection_state

    def get_chunks(self):
        if self.connecting():
            try:
                sqlinit = Path("init.sql").read_text(encoding="UTF-8")
                self.curr.execute(f"{sqlinit}")
                print("Connected to the PostgreSQL database")
            except (Exception, psy.DatabaseError) as error:
                raise error

        self.curr.execute("SELECT * FROM python.dbrag;")

    def create_chunks(self, data: list[Document]):

        client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

        if self.curr.pgresult_ptr is not None:
            for index, chunk in enumerate(data):
                response = client.models.embed_content(
                    model="gemini-embedding-001",
                    contents=chunk.page_content,
                )
                embeddings = response.embeddings[0].values
                self.curr.execute(
                    """
                                  INSERT INTO python.dbrag 
                                  (chunk_id,content,source,filename,embedding)
                                  VALUES (%s, %s, %s, %s, %s)
                                  """,
                    (
                        index,
                        chunk.page_content,
                        chunk.metadata["source"],
                        chunk.metadata["filename"],
                        embeddings,
                    ),
                )
