from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from tennis_scoreboard.application.repositories.repo_protocols import MatchRepoProtocol
from tennis_scoreboard.core.models.match import Match
from tennis_scoreboard.core.models.player import Player


class SqlaMatchRepo(MatchRepoProtocol):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_uuid(self, match_uuid: UUID) -> Match | None:
        stmt = select(Match).where(Match.uuid == match_uuid)
        return self._session.scalar(stmt)

    def add(self, match_: Match) -> None:
        self._session.add(match_)

    def get_page(
        self,
        player_name: str | None,
        limit: int,
        offset: int
    ) -> tuple[list[Match], int]:
        stmt = select(Match).options(
            joinedload(Match.first_player),
            joinedload(Match.second_player),
            joinedload(Match.winner)
        )
        count_stmt = select(func.count()).select_from(Match)

        if player_name:
            player_filter = or_(
                Match.first_player.has(Player.name == player_name),
                Match.second_player.has(Player.name == player_name),
            )
            stmt = stmt.where(player_filter)
            count_stmt = count_stmt.where(player_filter)

        stmt = stmt.order_by(Match.id.desc()).limit(limit).offset(offset)

        matches = list(self._session.scalars(stmt).unique().all())
        total = self._session.scalar(count_stmt) or 0

        return matches, total
