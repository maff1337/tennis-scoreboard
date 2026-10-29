from tennis_scoreboard.application.dto import MatchDto, MatchPage
from tennis_scoreboard.application.uow.uow_factory import UowFactory


class GetMatchesUseCase:
    PAGE_SIZE = 10

    def __init__(self, uow_factory: UowFactory) -> None:
        self._uow_factory = uow_factory

    def __call__(self, player_name: str | None, page: int) -> MatchPage:
        page = max(page, 1)

        with self._uow_factory() as uow:
            matches, total = uow.matches.get_page(
                player_name or None,
                self.PAGE_SIZE,
                (page-1) * self.PAGE_SIZE
            )
            return MatchPage(
                [MatchDto.from_model(m) for m in matches],
                total,
                page,
                self.PAGE_SIZE
            )
