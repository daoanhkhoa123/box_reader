
# import logging
# from typing_extensions import Self

# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, sessionmaker

# from src.configs.envs import EnvConfig
# from src.domain.unit_of_work import BaseUnitOfWork, BaseUnitOfWorkFactory
# from src.infrastructure.database.repositories import NewsRepository

# logger = logging.getLogger(__name__)

# engine = create_engine(
#     EnvConfig.database_url,
#     isolation_level="REPEATABLE READ",
# )

# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
# )

# class SqlAlchemyUnitOfWork(BaseUnitOfWork):
#     def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
#         self.session_factory = session_factory
#         self.logger = logger.getChild(self.__class__.__name__)

#         self.logger.debug(
#             "Initialized with session_factory=%s",
#             session_factory,
#         )

#     def __enter__(self) -> Self:
#         self.logger.debug("Entering unit of work")

#         self.session: Session = self.session_factory()
#         self.news_repository = NewsRepository(self.session)

#         self.logger.debug(
#             "Session created %s, repositories initialized",
#             self.session,
#         )

#         return self

#     def __exit__(self, exc_type, exc, tb):
#         if exc:
#             self.logger.error(
#                 "Exception detected, rolling back transaction",
#                 exc_info=(exc_type, exc, tb),
#             )
#             self.rollback()
#         else:
#             self.logger.debug("Exiting unit of work cleanly")

#         self.session.close()
#         self.logger.debug("Session closed")

#     def commit(self) -> None:
#         self.logger.debug("Committing transaction")
#         self.session.commit()
#         self.logger.info("Transaction committed")

#     def rollback(self) -> None:
#         self.logger.warning("Rolling back transaction")
#         self.session.rollback()


# class SqlAlchemyUnitOfWorkFactory(BaseUnitOfWorkFactory):
#     def __call__(self) -> SqlAlchemyUnitOfWork:
#         return SqlAlchemyUnitOfWork()
