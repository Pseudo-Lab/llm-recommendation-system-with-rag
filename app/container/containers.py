import os
from dependency_injector import containers, providers
from app.database.database import Database
from app.repository.movie_repository import MovieRepository
from app.service.movie_service import MovieService
# from app.repository.test_repository import TestRepository
# from app.service.test_service import TestService
from app.service.vector_service import VectorService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "app.api.v1.vector_api",
        # "app.api.v1.test_api",
    ])
    db = providers.Singleton(Database, db_url=os.getenv("MYSQL_DB_URL"))

    #repository
    movie_repository = providers.Factory(MovieRepository, session_factory=db.provided.session)
    # test_repository = providers.Factory(TestRepository, session_factory=db.provided.session)


    #service
    movie_service = providers.Factory(MovieService, movie_repository=movie_repository)
    # test_service = providers.Factory(TestService, test_repository=test_repository)

    vector_service = providers.Factory(VectorService, movie_service=movie_service)