import uuid
import os
from typing import List
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import (
    ElasticSearchBM25Retriever,
)
from langchain_openai import OpenAIEmbeddings
from tqdm import tqdm

from service.movie_service import MovieService
from utils.data import convert_to_dicts
from vector.vector_store import VectorStoreInterface
from langchain_core.documents import Document


class Elasticsearch(VectorStoreInterface):
    ES_URL = os.getenv("ES_URL")
    # ES_URL = "http://127.0.0.1:9200"
    async def create_vector(self, workspace_id: uuid.UUID, docs: List[Document], offset=100):
        index_name = f"{workspace_id}"
        vs = ElasticsearchStore(
            es_url=self.ES_URL,
            index_name=index_name,
            embedding=OpenAIEmbeddings(),
            # es_user="elastic",
            es_password="movie"
        )
        for i in tqdm(range(len(docs) // offset + 1)):
            s = i * offset
            e = min((i + 1) * offset, len(docs))
            await vs.aadd_documents(
                documents=docs[s:e]
            )
        vs.client.indices.refresh(index=index_name)
        return vs

    def create_bm25(self, workspace_id: uuid.UUID, docs: List[Document]):
        index_name = f"{workspace_id}"
        es_bm25 = ElasticSearchBM25Retriever.create(
            elasticsearch_url=self.ES_URL,
            index_name=index_name
        )
        es_bm25.add_texts()

    def get_vector_store(self, workspace_id: uuid.UUID):
        elastic_vector_search = ElasticsearchStore(
            es_url=self.ES_URL,
            index_name=f"{workspace_id}",
            embedding=OpenAIEmbeddings(),
            # es_user="elastic",
            es_password="movie"
        )
        return elastic_vector_search

    # def vector_cnt(self, workspace_id):
    #     vs = self.get_vector_store(workspace_id)
    #     vector_cnt = len(vs)
    #     return f'{vector_cnt} vector'

    async def transform_to_vectors(self):
        # 조회
        #TODO DI 순환참조 해결
        movies = self.movie_service.get_movie_info()
        docs = convert_to_dicts(movies)

        workspace_id = uuid.uuid4()
        await self.create_vector(workspace_id=workspace_id, docs=docs)
        # vs = self.get_vector_store(workspace_id=workspace_id)
        # print(len(docs))
        # result = await vs.aadd_documents(docs)
        # print(result)
        # for i in tqdm(range(len(metadatas) // 1000 + 1)):
        #     s = i * 1000
        #     e = min((i + 1) * 1000, len(metadatas))
        #     vs.add_texts(
        #         texts=texts[s:e],
        #         metadatas=metadatas[s:e]
        #     )
        return {"workspace_id": workspace_id}
