from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from tennis_scoreboard.core.models.match import Match
from tennis_scoreboard.core.models.player import Player


class MatchRepoProtocol(Protocol):
    @abstractmethod
    def get_by_uuid(self, match_uuid: UUID) -> Match | None:
        ...

    @abstractmethod
    def get_page(
        self,
        player_name: str | None,
        limit: int,
        offset: int
    ) -> tuple[Sequence[Match], int]:
        ...

    @abstractmethod
    def add(self, match_: Match) -> None:
        ...


class PlayerRepoProtocol(Protocol):
    @abstractmethod
    def add(self, player: Player) -> None:
        ...

    @abstractmethod
    def get_by_name(self, name: str) -> Player | None:
        ...
