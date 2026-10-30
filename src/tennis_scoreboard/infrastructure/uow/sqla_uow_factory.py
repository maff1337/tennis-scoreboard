from sqlalchemy.orm import sessionmaker

from tennis_scoreboard.application.repositories.repo_factories import (
    MatchRepoFactory,
    PlayerRepoFactory,
)
from tennis_scoreboard.application.uow.uow_factory import UowFactory
from tennis_scoreboard.application.uow.uow_protocol import UnitOfWork
from tennis_scoreboard.di import inject
from tennis_scoreboard.infrastructure.uow.sqla_uow import SqlaUnitOfWork


@inject
class SqlaUowFactory(UowFactory):
    def __init__(
        self,
        session_factory: sessionmaker,
        players_factory: PlayerRepoFactory,
        matches_factory: MatchRepoFactory,
    ) -> None:
        self._session_factory = session_factory
        self._players_factory = players_factory
        self._matches_factory = matches_factory

    def __call__(self) -> UnitOfWork:
        return SqlaUnitOfWork(
            self._session_factory,
            self._players_factory,
            self._matches_factory,
        )
