import os
import uuid
from tqdm import tqdm
from langchain.chains.query_constructor.base import get_query_constructor_prompt, StructuredQueryOutputParser

from utils.self_query import metadata_field_info
from langchain.retrievers import SelfQueryRetriever
from langchain_openai import ChatOpenAI
from database.chroma_db import ChromaDB
from service.movie_service import MovieService
from utils.data import convert_to_dicts


class VectorService:
    def __init__(self, movie_service: MovieService):
        self.movie_service = movie_service
    def create_vector(self, text):
        return text

    def get_vector(self, workspace_id: uuid.uuid4()):
        vector_db = ChromaDB.get_vectorstore(
            vector_path= f'{os.getenv("VECTOR_DB_PATH_PREFIX")}{workspace_id}'
        )
        return vector_db



    # def update_vector(self, vector_id: int, new_vector: Vector):
    #     pass

    def delete_vector(self, vector_id: int):
        pass
        # for i, vector in enumerate(self.db):
        #     if vector.id == vector_id:
        #         return self.db.pop(i)
        # return None

    def get_all_vectors(self):
        pass
        # return self.db

    def transform_to_vectors(self):
        # 조회
        movies = self.movie_service.get_movie_info()
        metadatas, texts = convert_to_dicts(movies)

        workspace_id = uuid.uuid4()
        vector_path = f'{os.getenv("VECTOR_DB_PATH_PREFIX")}{workspace_id}'
        vs = ChromaDB.get_vectorstore(vector_path)

        for i in tqdm(range(len(metadatas)//1000 + 1)):
            s = i * 1000
            e = min((i+1) * 1000, len(metadatas))
            vs.add_texts(
                texts=texts[s:e],
                metadatas=metadatas[s:e]
            )
        return {"workspace_id": workspace_id}

    def similarity_search(self, workspace_id: uuid.UUID, text: str, k:int):
        vs = self.get_vector(workspace_id=workspace_id)
        docs = vs.similarity_search_with_score(text, k=k)
        return docs

    async def similarity_search_with_self_query(self, workspace_id, input):
        document_content_description = "질의와 관련된 영화를 추천해줘"
        vs = self.get_vector(workspace_id=workspace_id)

        model = ChatOpenAI(
            temperature=0,
            model_name=os.getenv("LLM_MODEL_NAME"),
            verbose=True
        )
        prompt = get_query_constructor_prompt(
            document_content_description,
            metadata_field_info,
        )
        output_parser = StructuredQueryOutputParser.from_components()
        query_constructor = prompt | model | output_parser
        response = await query_constructor.ainvoke(input)
        print(prompt.format(query=input))
        print(response)
        # retriever = SelfQueryRetriever.from_llm(
        #     model,
        #     vs,
        #     document_content_description,
        #     metadata_field_info,
        #     enable_limit=True,
        #     search_kwargs={"k": 2}
        # )
        # return await retriever.ainvoke(input)

    def vector_cnt(self, workspace_id):
        vs = self.get_vector(workspace_id)
        vector_cnt = len(vs)
        return f'{vector_cnt} vector'


