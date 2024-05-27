import os
import uuid
from tqdm import tqdm
from utils.data import convert_to_dicts
from vector.vector_store import VectorStoreInterface


class ChromaVector(VectorStoreInterface):
    def create_vector(self, text):
        return text

    def get_vector_store(self, workspace_id: uuid.UUID):
        vector_db = ChromaDB.get_vectorstore(
            vector_path=f'{os.getenv("VECTOR_DB_PATH_PREFIX")}{workspace_id}'
        )
        return vector_db

    def transform_to_vectors(self):
        # 조회
        movies = self.movie_service.get_movie_info()
        metadatas, texts = convert_to_dicts(movies)

        workspace_id = uuid.uuid4()
        vector_path = f'{os.getenv("VECTOR_DB_PATH_PREFIX")}{workspace_id}'
        # vs = ChromaDB.get_vectorstore(vector_path)

        for i in tqdm(range(len(metadatas)//1000 + 1)):
            s = i * 1000
            e = min((i+1) * 1000, len(metadatas))
            vs.add_texts(
                texts=texts[s:e],
                metadatas=metadatas[s:e]
            )
        return {"workspace_id": workspace_id}

    def vector_cnt(self, workspace_id):
        vs = self.get_vector(workspace_id)
        vector_cnt = len(vs)
        return f'{vector_cnt} vector'


