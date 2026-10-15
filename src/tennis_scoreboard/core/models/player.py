from itertools import chain
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from tennis_scoreboard.core.models.base import Base
from tennis_scoreboard.core.valiators.lang_validator import has_single_alphabet

if TYPE_CHECKING:
    from tennis_scoreboard.core.models.match import Match


class Player(Base):
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    matches: Mapped[list["Match"]] = relationship(
        primaryjoin="or_("
                    "Player.id == Match.first_player_id, "
                    "Player.id == Match.second_player_id"
                    ")",
        foreign_keys="[Match.first_player_id, Match.second_player_id]",
        viewonly=True
    )

    @validates('name')
    def validate_name(self, key: str, value: str) -> str:
        value = value.strip()

        if not 1 <= len(value) <= 100:
            raise Exception('Name must contain between 1 and 100 characters')

        if not all(map(
            str.isalpha,
            chain.from_iterable(
                [
                    s.split('-')
                    for s in value.split()
                ]
            )
        )
        ):
            raise Exception('Name must contain only letters and separators')

        if not has_single_alphabet(value):
            raise Exception('Name must use only Latin or Cyrillic letters')

        return value
