import os
from typing import Optional, Union
import psycopg2 as psy
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


class SQL_Injection:

    def __init__(
        self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str
    ) -> None:
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def psql_connection(self):
        try:
            return psy.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
        except Exception as e:
            connection_state = False
            logger.error("Database Error connection failed: %s", e)
            raise RuntimeError("Database Error connection failed") from e

    def sql_table_init(self):
        try:
            with self.psql_connection() as connect:
                with connect.cursor() as cursor:
                    sqlinit = Path("init.sql").read_text(encoding="UTF-8")
                    cursor.execute(f"{sqlinit}")
                    print("Connected to the PostgreSQL database")
        except psy.DatabaseError as error:
            logger.error("Database Error init failed: %s", error)
            raise psy.DatabaseError(f"{error}")

    def create_chunks(self, *args):

        if self.psql_connection() is not None:
            with self.psql_connection() as connect:
                with connect.cursor() as cursor:
                    cursor.execute(
                        """
                                  INSERT INTO python.dbrag 
                                  (chunk_id,content,source,filename,embedding)
                                  VALUES (%s, %s, %s, %s, %s)
                                  """,
                        (args),
                    )
        else:
            logger.error("chunking tidak dapat diimplementasikan")
