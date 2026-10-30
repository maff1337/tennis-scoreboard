from dataclasses import dataclass
from typing import Self
from uuid import UUID

from tennis_scoreboard.core.vo.score import Score


@dataclass(frozen=True)
class MatchDto:
    uuid: UUID
    first_player: str
    second_player: str
    score: Score
    winner: str | None

    @classmethod
    def from_model(cls, model) -> Self:
        return cls(
            uuid=model.uuid,
            first_player=model.first_player.name,
            second_player=model.second_player.name,
            score=model.score,
            winner=model.winner.name if model.winner else None,
        )


@dataclass(frozen=True)
class MatchPage:
    items: list[MatchDto]
    total: int
    page: int
    page_size: int

    @property
    def pages(self) -> int:
        return max(1, -(-self.total // self.page_size))
