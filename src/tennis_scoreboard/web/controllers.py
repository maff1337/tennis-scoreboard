from http import HTTPStatus
from uuid import UUID

from tennis_scoreboard.application.use_cases.create_match import CreateMatchUseCase
from tennis_scoreboard.application.use_cases.get_match_score import GetMatchScoreUseCase
from tennis_scoreboard.application.use_cases.get_matches import GetMatchesUseCase
from tennis_scoreboard.application.use_cases.register_point import RegisterPointUseCase
from tennis_scoreboard.di import inject
from tennis_scoreboard.exceptions import (
    HttpError,
    MatchAlreadyFinishedError,
    PlayerValidationError,
    SamePlayersError,
)
from tennis_scoreboard.web.presenters import render_points
from tennis_scoreboard.web.renderer import TemplateRenderer
from tennis_scoreboard.web.types import Request, Response


def _match_url(match_uuid: UUID) -> str:
    return f'/match-score?uuid={match_uuid}'


def _parse_uuid(request: Request) -> UUID:
    try:
        return UUID(request.query.get('uuid', ''))
    except ValueError:
        raise HttpError(HTTPStatus.NOT_FOUND, 'Match not found') from None


@inject
class MatchController:
    def __init__(
        self,
        create_match: CreateMatchUseCase,
        get_match_score: GetMatchScoreUseCase,
        register_point: RegisterPointUseCase,
        get_matches: GetMatchesUseCase,
        view: TemplateRenderer
    ) -> None:
        self._create_match = create_match
        self._get_match_score = get_match_score
        self._register_point = register_point
        self._get_matches = get_matches
        self._view = view

    def new_match_form(self, request: Request) -> Response:
        return self._view.render('new_match.html', error=None, first='', second='')

    def create_match(self, request: Request) -> Response:
        first = request.form.get('first_player_name', '')
        second = request.form.get('second_player_name', '')

        try:
            match_uuid = self._create_match(first, second)
        except (PlayerValidationError, SamePlayersError) as e:
            return self._view.render(
                'new_match.html',
                HTTPStatus.BAD_REQUEST,
                first=first,
                second=second,
                error=str(e)
            )

        return Response.redirect(_match_url(match_uuid))

    def match_score(self, request: Request) -> Response:
        match_ = self._get_match_score(_parse_uuid(request))

        return self._view.render(
            'match_score.html',
            match=match_,
            points=render_points(match_.score)
        )

    def add_point(self, request: Request) -> Response:
        match_uuid = _parse_uuid(request)

        try:
            self._register_point(
                match_uuid, request.form.get('winner_name', ''))
        except MatchAlreadyFinishedError:
            pass

        return Response.redirect(_match_url(match_uuid))

    def matches(self, request: Request) -> Response:
        try:
            page = int(request.query.get('page', '1'))
        except ValueError:
            page = 1

        player_name = request.query.get('player-name', '').strip()
        result = self._get_matches(player_name or None, page)

        return self._view.render(
            'matches.html',
            result=result,
            player_name=player_name
        )
