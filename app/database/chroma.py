from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List
# https://python.langchain.com/docs/integrations/vectorstores/chroma/
class Rag_Chroma:
    # def __init__(self, vector_path):
    #     self.vector_path = vector_path

    @staticmethod
    def get_vectorstore(vector_db_path):
        vectorstore = Chroma(
            persist_directory=vector_db_path,
            embedding_function=OpenAIEmbeddings()
        )
        return vectorstore

    def create_vectorstore(self, vector_db_path: str, chunks: List[str]):
        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=OpenAIEmbeddings(),
            persist_directory=vector_db_path
        )
        vectorstore.persist()
        return vectorstore

