from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from tennis_scoreboard.application.repositories.repo_factories import (
    MatchRepoFactory,
    PlayerRepoFactory,
)
from tennis_scoreboard.application.uow.uow_protocol import UnitOfWork


class SqlaUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        players_factory: PlayerRepoFactory,
        matches_factory: MatchRepoFactory,
    ) -> None:
        self._session_factory = session_factory
        self._players_factory = players_factory
        self._matches_factory = matches_factory

        self._session: Session | None = None

        self._players = None
        self._matches = None

    def __enter__(self) -> Self:
        if self._session is not None:
            raise RuntimeError('UOW is already entered')

        self._session = self._session_factory()
        self._players = self._players_factory(self._session)
        self._matches = self._matches_factory(self._session)

        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        session = self._require_session()

        try:
            if exc_type is not None:
                session.rollback()
        finally:
            session.close()
            self._session = self._players = self._matches = None

    @property
    def players(self):
        self._require_session()
        assert self._players is not None
        return self._players

    @property
    def matches(self):
        self._require_session()
        assert self._matches is not None
        return self._matches

    def commit(self) -> None:
        self._require_session().commit()

    def rollback(self) -> None:
        self._require_session().rollback()

    def _require_session(self) -> Session:
        if self._session is None:
            raise RuntimeError(
                "UOW must be used as a context manager: `with uow: ...`")

        return self._session
