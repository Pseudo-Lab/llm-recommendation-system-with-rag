from dependency_injector import containers, providers
from app.service.vector_service import VectorService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["app.api.v1.vector.api"])

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