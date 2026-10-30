from abc import abstractmethod
from typing import Protocol, Self

from tennis_scoreboard.application.repositories.repo_protocols import (
    MatchRepoProtocol,
    PlayerRepoProtocol,
)


class UnitOfWork(Protocol):
    @property
    @abstractmethod
    def players(self) -> PlayerRepoProtocol:
        ...

    @property
    @abstractmethod
    def matches(self) -> MatchRepoProtocol:
        ...

    @abstractmethod
    def __enter__(self) -> Self:
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc, tb) -> None:
        ...

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...
