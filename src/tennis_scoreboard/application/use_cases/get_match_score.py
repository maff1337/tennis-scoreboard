from uuid import UUID

from tennis_scoreboard.application.dto import MatchDto
from tennis_scoreboard.application.uow.uow_factory import UowFactory
from tennis_scoreboard.di import inject
from tennis_scoreboard.exceptions import MatchNotFoundError


@inject
class GetMatchScoreUseCase:
    def __init__(self, uow_factory: UowFactory) -> None:
        self._uow_factory = uow_factory

    def __call__(self, match_uuid: UUID) -> MatchDto:
        with self._uow_factory() as uow:
            match_ = uow.matches.get_by_uuid(match_uuid)
            if match_ is None:
                raise MatchNotFoundError(f'Match {match_uuid} not found')
            return MatchDto.from_model(match_)
