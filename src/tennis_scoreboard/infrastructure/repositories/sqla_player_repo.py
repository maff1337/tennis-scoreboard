from sqlalchemy import select
from sqlalchemy.orm import Session

from tennis_scoreboard.application.repositories.repo_protocols import PlayerRepoProtocol
from tennis_scoreboard.core.models.player import Player


class SqlaPlayerRepo(PlayerRepoProtocol):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_name(self, name: str) -> Player | None:
        stmt = select(Player).where(Player.name == name)
        return self._session.scalar(stmt)

    def add(self, player: Player) -> None:
        self._session.add(player)
