import os
from dependency_injector import containers, providers
from app.database.database import Database
from app.repository.movie_repository import MovieRepository
from app.service.gen_service import GenService
from app.service.movie_service import MovieService
from app.service.rag_interface import OpenAIRag
# from app.repository.test_repository import TestRepository
# from app.service.test_service import TestService
from app.service.vector_service import VectorService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[
        "app.api.v1.vector_api",
        "app.api.v1.generate_api",
        # "app.api.v1.test_api",
    ])
    db = providers.Singleton(
        Database,
        db_url=config.db_url
    )

    #repository
    movie_repository = providers.Factory(MovieRepository, session_factory=db.provided.session)
    # test_repository = providers.Factory(TestRepository, session_factory=db.provided.session)

    #service
    movie_service = providers.Factory(MovieService, movie_repository=movie_repository)
    vector_service = providers.Factory(VectorService, movie_service=movie_service)
    # test_service = providers.Factory(TestService, test_repository=test_repository)


    # interface
    rag_template = providers.Factory(OpenAIRag, vector_service=vector_service)

    gen_service = providers.Factory(GenService, vector_service=vector_service, rag=rag_template)