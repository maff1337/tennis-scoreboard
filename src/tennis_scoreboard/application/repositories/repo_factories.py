from abc import abstractmethod
from typing import Protocol

from sqlalchemy.orm import Session

from tennis_scoreboard.application.repositories.repo_protocols import (
    MatchRepoProtocol,
    PlayerRepoProtocol,
)


class PlayerRepoFactory(Protocol):
    @abstractmethod
    def __call__(self, session: Session) -> PlayerRepoProtocol:
        ...


class MatchRepoFactory(Protocol):
    @abstractmethod
    def __call__(self, session: Session) -> MatchRepoProtocol:
        ...
