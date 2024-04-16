from app.service.movie_service import MovieService


class VectorService:
    def __init__(self, movie_service: MovieService):
        self.movie_service = movie_service
    def create_vector(self, text):
        return text

    def get_vector(self):
        pass

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
        for movie, synopsis_prep in movies[0:2]:
            print("Movie ID:", movie.movieId)
            print("Title (Korean):", movie.titleKo)
            print("Title (English):", movie.titleEn)
            print("Synopsis:", movie.synopsis)
            print("Cast:", movie.cast)
            print("Main Page URL:", movie.mainPageUrl)
            print("Poster URL:", movie.posterUrl)
            print("Number of Site Ratings:", movie.numOfSiteRatings)
            print("Synopsis Preparation:", synopsis_prep.synopsis_prep)
            print("\n")

        # vector_db 전환

        # return path

