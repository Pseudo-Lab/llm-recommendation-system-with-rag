import os
import uuid

from app.database.chroma_db import ChromaDB
from app.service.movie_service import MovieService


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
        metadatas = []
        texts = []
        for movie, synopsis_prep in movies[0:10]:
            movie_dic = {
                "movieId" : movie.movieId,
                "titleKo" : movie.titleKo,
                "titleEn" : movie.titleEn,
                "synopsis" : movie.synopsis,
                "cast" : movie.cast,
                "mainPageUrl" : movie.mainPageUrl,
                "posterUrl" : movie.posterUrl,
                "numOfSiteRatings" : movie.numOfSiteRatings,
            }
            metadatas.append(movie_dic)
            texts.append(synopsis_prep.synopsis_prep)

        workspace_id = uuid.uuid4()
        vector_path = f'{os.getenv("VECTOR_DB_PATH_PREFIX")}{workspace_id}'
        ChromaDB.create_vectorstore(
            vector_path=vector_path,
            texts=texts,
            metadatas=metadatas
        )
        # query = "영화 아무거나 추천해줘?"
        # docs = vector_db.similarity_search(query)
        # print(docs)
        return {"workspace_id": workspace_id}
