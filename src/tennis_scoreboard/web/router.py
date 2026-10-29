from collections.abc import Callable
from http import HTTPStatus

from tennis_scoreboard.exceptions import HttpError
from tennis_scoreboard.web.types import Request, Response

Handler = Callable[[Request], Response]


class Router:
    def __init__(self) -> None:
        self._routes: dict[str, dict[str, Handler]] = {}

    def add(self, method: str, path: str, handler: Handler) -> None:
        self._routes.setdefault(path, {})[method.upper()] = handler

    def resolve(self, method: str, path: str) -> Handler:
        methods = self._routes.get(path.rstrip('/') or '/')

        if methods is None:
            raise HttpError(HTTPStatus.NOT_FOUND)

        handler = methods.get(method)

        if handler is None:
            raise HttpError(HTTPStatus.METHOD_NOT_ALLOWED)

        return handler
