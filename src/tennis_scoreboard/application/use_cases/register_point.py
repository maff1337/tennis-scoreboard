from uuid import UUID

from tennis_scoreboard.application.dto import MatchDto
from tennis_scoreboard.application.uow import UowFactory
from tennis_scoreboard.core.services.score_service import ScoreService
from tennis_scoreboard.exceptions import MatchNotFoundError


class RegisterPointUseCase:
    def __init__(self, uow_factory: UowFactory, score_service: ScoreService) -> None:
        self._uow_factory = uow_factory
        self._score_service = score_service

    def __call__(self, match_uuid: UUID, winner_name: str) -> MatchDto:
        with self._uow_factory() as uow:
            match_ = uow.matches.get_by_uuid(match_uuid)
            if match_ is None:
                raise MatchNotFoundError(f'Match {match_uuid} not found')
            self._score_service(match_, winner_name)
            uow.commit()
            return MatchDto.from_model(match_)
