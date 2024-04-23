from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from app.model.model import DaumMovie, DaumMovieSynopsisPrep


class MovieRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_movie_info(self) -> List:
        with self.session_factory() as session:
            # result = session.query(DaumMovie).join(DaumMovieSynopsisPrep).filter(
            #     DaumMovie.movieId == DaumMovieSynopsisPrep.movieId).all()
            result = session.query(DaumMovie, DaumMovieSynopsisPrep).outerjoin(DaumMovieSynopsisPrep).all()
            # result = session.query(DaumMovie).all()
            if not result:
                raise ValueError("empty")
            return result
