from abc import abstractmethod
from typing import Protocol

from tennis_scoreboard.application.uow.uow_protocol import UnitOfWork


class UowFactory(Protocol):
    @abstractmethod
    def __call__(self) -> UnitOfWork:
        ...
