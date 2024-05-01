from repository.movie_repository import MovieRepository


class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def get_movie_info(self):
        return self.movie_repository.get_movie_info()