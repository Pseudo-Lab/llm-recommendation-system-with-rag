import os
import uuid

from app.database.chroma_db import ChromaDB
from app.service.movie_service import MovieService
from app.utils.data import convert_to_dicts


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
        ChromaDB.create_vectorstore(
                vector_path=vector_path,
                texts=texts,
                metadatas=metadatas
        )
        return {"workspace_id": workspace_id}

    def similarity_search(self, workspace_id: uuid.UUID, text: str):
        vs = self.get_vector(workspace_id=workspace_id)
        docs = vs.similarity_search(text)
        return docs
