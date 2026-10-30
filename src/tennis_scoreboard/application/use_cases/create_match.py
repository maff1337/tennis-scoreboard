from uuid import UUID, uuid4

from tennis_scoreboard.application.uow.uow_factory import UowFactory
from tennis_scoreboard.application.uow.uow_protocol import UnitOfWork
from tennis_scoreboard.core.models.match import Match
from tennis_scoreboard.core.models.player import Player
from tennis_scoreboard.core.vo.score import Score
from tennis_scoreboard.di import inject
from tennis_scoreboard.exceptions import SamePlayersError


@inject
class CreateMatchUseCase:
    def __init__(self, uow_factory: UowFactory) -> None:
        self._uow_factory = uow_factory

    def __call__(self, first_name: str, second_name: str) -> UUID:
        first_name, second_name = first_name.strip(), second_name.strip()

        if first_name.casefold() == second_name.casefold():
            raise SamePlayersError('Players must be different')

        with self._uow_factory() as uow:
            first = self._get_or_create(uow, first_name)
            second = self._get_or_create(uow, second_name)

            match_ = Match(
                uuid=uuid4(),
                first_player=first,
                second_player=second,
                score=Score(),
            )

            uow.matches.add(match_)
            uow.commit()
            return match_.uuid

    @staticmethod
    def _get_or_create(uow: UnitOfWork, name: str) -> Player:
        player = uow.players.get_by_name(name)

        if player is None:
            player = Player(name=name)
            uow.players.add(player)

        return player
