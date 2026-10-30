from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tennis_scoreboard.core.models.base import Base
from tennis_scoreboard.core.vo.score import Score
from tennis_scoreboard.infrastructure.database.types import ScoreType

if TYPE_CHECKING:
    from tennis_scoreboard.core.models.player import Player


class Match(Base):
    __tablename__ = 'matches'

    __table_args__ = (
        CheckConstraint(
            'first_player_id != second_player_id',
            name='check_different_players',
        ),
        CheckConstraint(
            'winner_id IS NULL '
            'OR winner_id = first_player_id '
            'OR winner_id = second_player_id',
            name='check_winner_is_game_player'
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(
        Uuid, default=uuid4, nullable=False, unique=True)

    first_player_id: Mapped[int] = mapped_column(
        ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    second_player_id: Mapped[int] = mapped_column(
        ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey('players.id'), nullable=True
    )
    score: Mapped[Score] = mapped_column(
        ScoreType,
        nullable=False
    )

    first_player: Mapped["Player"] = relationship(
        foreign_keys=[first_player_id]
    )

    second_player: Mapped["Player"] = relationship(
        foreign_keys=[second_player_id]
    )

    winner: Mapped["Player | None"] = relationship(
        foreign_keys=[winner_id]
    )
