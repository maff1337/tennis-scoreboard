from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tennis_scoreboard.core.models.base import Base

if TYPE_CHECKING:
    from tennis_scoreboard.core.models.match import Match


class Player(Base):
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    matches: Mapped[list["Match"]] = relationship(
        primaryjoin="or_("
                    "Player.id == Match.first_player_id, "
                    "Player.id == Match.second_player_id"
                    ")",
        foreign_keys="[Match.first_player_id, Match.second_player_id]",
        viewonly=True
    )
