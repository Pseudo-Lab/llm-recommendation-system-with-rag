from abc import *
import uuid

from langchain_core.vectorstores import VectorStore


class VectorStoreInterface(metaclass=ABCMeta):
    def __init__(self, movie_service):
        self.movie_service = movie_service

    @abstractmethod
    def create_vector(self, **kwargs):
        '''
        vector 생성
        :param text:
        :return:
        '''
        pass

    @abstractmethod
    def get_vector_store(self, workspace_id: uuid.UUID, strategy) -> VectorStore:
        '''
        vector 가져오기
        :param workspace_id:
        :return:
        '''
        pass

    def vector_cnt(self, workspace_id: uuid.UUID):
        '''
        vector 데이터 개수 카운트
        :param workspace_id:
        :return:
        '''
        pass

    @abstractmethod
    def transform_to_vectors(self):
        '''
        데이터를 벡터로 전환
        :return:
        '''
        pass
