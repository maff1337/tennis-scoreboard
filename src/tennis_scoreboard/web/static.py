import mimetypes
from http import HTTPStatus
from pathlib import Path

from tennis_scoreboard.exceptions import HttpError
from tennis_scoreboard.web.types import Response


class StaticFiles:
    def __init__(self, root: Path, url_prefix: str = '/static/') -> None:
        self._root = root.resolve()
        self._url_prefix = url_prefix

    def matches(self, path: str) -> bool:
        return path.startswith(self._url_prefix)

    def serve(self, path: str) -> Response:
        relative = path.removeprefix(self._url_prefix)

        try:
            target = (self._root / relative).resolve()

            if not target.is_relative_to(self._root) or not target.is_file():
                raise HttpError(HTTPStatus.NOT_FOUND)

            body = target.read_bytes()
        except (ValueError, OSError):
            raise HttpError(HTTPStatus.NOT_FOUND) from None

        content_type = (mimetypes.guess_type(target.name)[0]
                        or 'application/octet-stream')

        if content_type.startswith('text/') or content_type in (
            'application/javascript', 'application/json'
        ):
            content_type += '; charset=utf-8'

        return Response(
            body,
            HTTPStatus.OK,
            [('Content-Type', content_type),
             ('Cache-Control', 'public, max-age=3600')]
        )
