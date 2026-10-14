from dataclasses import asdict
from typing import Any

from sqlalchemy import JSON, Dialect, TypeDecorator

from tennis_scoreboard.core.vo.score import Games, Points, Score, Sets


class ScoreType(TypeDecorator[Score]):
    impl = JSON
    cache_ok = True

    def process_bind_param(self, value: Score | None, dialect: Dialect) -> dict[str, dict[str, int]] | None:
        if value is None:
            return None

        return asdict(value)

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Score | None:
        if value is None:
            return None

        return Score(
            sets=Sets(**value['sets']),
            games=Games(**value['games']),
            points=Points(**value['points'])
        )
