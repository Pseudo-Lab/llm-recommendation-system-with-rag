import os
from dependency_injector import containers, providers
from app.database.database import Database
from app.repository.test_repository import TestRepository
from app.service.test_service import TestService
from app.service.vector_service import VectorService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "app.api.v1.vector_api",
        "app.api.v1.test_api",
    ])
    db = providers.Singleton(Database, db_url=os.getenv("MYSQL_DB_URL"))

    #repository
    test_repository = providers.Factory(TestRepository, session_factory=db.provided.session)


    #service
    test_service = providers.Factory(TestService, test_repository=test_repository)

    vector_service = providers.Factory(
        VectorService
    )


    # config = providers.Configuration(yaml_files=["config.yml"])

    # db = providers.Singleton(Database, db_url=config.db.url)

    # user_repository = providers.Factory(
    #     UserRepository,
    #     session_factory=db.provided.session,
    # )
    #
    # user_service = providers.Factory(
    #     UserService,
    #     user_repository=user_repository,
    # )