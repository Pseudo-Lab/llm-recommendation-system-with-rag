from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


class BgeM3Embeddings(HuggingFaceEmbeddings):
    def __init__(self):
        super().__init__(
            model_name='BAAI/bge-m3',
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True},
        )


class ChatGPTEmbeddings(OpenAIEmbeddings):
    pass