import logging
from collections.abc import Callable
from http import HTTPStatus

from tennis_scoreboard.exceptions import (
    HttpError,
    MatchAlreadyFinishedError,
    MatchNotFoundError,
    PlayerNotInMatchError,
    PlayerValidationError,
    SamePlayersError,
)
from tennis_scoreboard.web.router import Router
from tennis_scoreboard.web.static import StaticFiles
from tennis_scoreboard.web.types import Request, Response

log = logging.getLogger(__name__)


ERROR_STATUS: list[tuple[type[Exception], HTTPStatus]] = [
    (MatchNotFoundError, HTTPStatus.NOT_FOUND),
    (MatchAlreadyFinishedError, HTTPStatus.CONFLICT),
    (PlayerNotInMatchError, HTTPStatus.BAD_REQUEST),
    (PlayerValidationError, HTTPStatus.BAD_REQUEST),
    (SamePlayersError, HTTPStatus.BAD_REQUEST)
]

ErrorPage = Callable[[HTTPStatus, str], Response]


class Application:
    def __init__(
        self,
        router: Router,
        static: StaticFiles,
        error_page: ErrorPage
    ) -> None:
        self._router = router
        self._static = static
        self._error_page = error_page

    def __call__(self, environ, start_response):
        try:
            response = self._handle(Request.from_environ(environ))
        except HttpError as e:
            response = self._error(e.status, str(e))
        except Exception as e:
            status = next(
                (s for exc_type, s in ERROR_STATUS if isinstance(e, exc_type)),
                None
            )

            if status is None:
                log.exception('Unhandled error')
                response = self._error(
                    HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error'
                )
            else:
                response = self._error(status, str(e))

        start_response(
            f'{response.status.value} {response.status.phrase}',
            [*response.headers, ('Content-Length', str(len(response.body)))]
        )

        return [response.body]

    def _handle(self, request: Request) -> Response:
        if self._static.matches(request.path) and request.method == 'GET':
            return self._static.serve(request.path)

        return self._router.resolve(request.method, request.path)(request)

    def _error(self, status: HTTPStatus, message: str) -> Response:
        try:
            return self._error_page(status, message)
        except Exception:
            log.exception('Cannot render error page')
            return Response.text(f'{status.value} {status.phrase}', status)
