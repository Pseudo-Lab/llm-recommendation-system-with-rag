from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from model.model import DaumMovie, DaumMovieSynopsisPrep


class MovieRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    # def get_movie_info(self) -> List:
    #     with self.session_factory() as session:
    #         offset = 0
    #         limit = 5000
    #         all_results = []
    #         while True:
    #             result = session.query(DaumMovie, DaumMovieSynopsisPrep).outerjoin(DaumMovieSynopsisPrep).offset(offset).limit(limit).all()
    #             if not result:
    #                 break
    #             all_results.extend(result)
    #             offset += limit
    #         if not all_results:
    #             raise ValueError("empty")
    #         return all_results

    def get_movie_info(self) -> List:
        with self.session_factory() as session:
            all_result = []
            results = session.query(DaumMovie, DaumMovieSynopsisPrep).outerjoin(DaumMovieSynopsisPrep).limit(100)
            all_result.extend(results)
            return all_result
