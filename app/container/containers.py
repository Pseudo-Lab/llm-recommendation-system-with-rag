from dependency_injector import containers, providers
from database.database import Database
from repository.movie_repository import MovieRepository
from service.gen_service import GenService
from service.movie_service import MovieService
from service.rag_interface import OpenAIRag
from service.retrieval_service import RetrievalService
from vector.chroma import ChromaVector
from vector.elasticsearch import Elasticsearch


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[
        "api.v1.vector_api",
        "api.v1.generate_api",
        "api.v1.retrieval_api"
        # "app.api.v1.test_api",
    ])
    db = providers.Singleton(
        Database,
        db_url=config.db_url
    )

    #repository
    movie_repository = providers.Factory(MovieRepository, session_factory=db.provided.session)

    #service
    movie_service = providers.Factory(MovieService, movie_repository=movie_repository)

    # vector
    vector_store = providers.Factory(Elasticsearch, movie_service=movie_service)

    #rag
    OpenAI_RAG = providers.Factory(OpenAIRag, vector_store=vector_store)

    retrieval_service = providers.Factory(RetrievalService, vector=vector_store)

    # interface
    gen_service = providers.Factory(GenService, rag=OpenAI_RAG)