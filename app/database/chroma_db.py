from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List
# https://python.langchain.com/docs/integrations/vectorstores/chroma/
class ChromaDB:
    # def __init__(self, vector_path):
    #     self.vector_path = vector_path

    @staticmethod
    def get_vectorstore(vector_path):
        vectorstore = Chroma(
            persist_directory=vector_path,
            embedding_function=OpenAIEmbeddings()
        )
        return vectorstore

    def create_vectorstore(self, vector_path: str, texts: List[str], metadatas: List[dict]):
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=OpenAIEmbeddings(),
            persist_directory=vector_path,
            metadatas=metadatas
        )
        vectorstore.persist()
        return vectorstore

