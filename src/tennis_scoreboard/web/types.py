from dataclasses import dataclass, field
from http import HTTPStatus
from urllib.parse import parse_qs

from tennis_scoreboard.exceptions import HttpError

MAX_BODY_SIZE = 8 * 1024
FORM_CONTENT_TYPE = 'application/x-www-form-urlencoded'


def _first_values(parsed: dict[str, list[str]]) -> dict[str, str]:
    return {key: value[0] for key, value in parsed.items()}


@dataclass(frozen=True)
class Request:
    method: str
    path: str
    query: dict[str, str]
    form: dict[str, str]

    @classmethod
    def from_environ(cls, environ: dict) -> 'Request':
        method = environ['REQUEST_METHOD'].upper()
        form: dict[str, str] = {}

        content_type: str = environ.get('CONTENT_TYPE', '')

        if method == 'POST' and content_type.startswith(FORM_CONTENT_TYPE):
            try:
                length = int(environ.get('CONTENT_LENGTH') or 0)
            except ValueError:
                raise HttpError(HTTPStatus.BAD_REQUEST) from None

            if length < 0:
                raise HttpError(HTTPStatus.BAD_REQUEST)

            if length > MAX_BODY_SIZE:
                raise HttpError(HTTPStatus(413))

            raw = environ['wsgi.input'].read(length).decode('utf-8', 'replace')
            form = _first_values(parse_qs(raw, keep_blank_values=True))

        query = parse_qs(environ.get('QUERY_STRING', ''),
                         keep_blank_values=True)

        return cls(
            method=method,
            path=environ.get('PATH_INFO', '/'),
            query=_first_values(query),
            form=form
        )


@dataclass
class Response:
    body: bytes = field(default=b'')
    status: HTTPStatus = field(default=HTTPStatus.OK)
    headers: list[tuple[str, str]] = field(default_factory=list)

    @classmethod
    def html(cls, text: str, status: HTTPStatus = HTTPStatus.OK) -> 'Response':
        return cls(
            text.encode('utf-8'),
            status,
            [('Content-Type', 'text/html; charset=utf-8')]
        )

    @classmethod
    def text(cls, text: str, status: HTTPStatus = HTTPStatus.OK) -> 'Response':
        return cls(
            text.encode('utf-8'),
            status,
            [('Content-Type', 'text/plain; charset=utf-8')],
        )

    @classmethod
    def redirect(cls, location: str) -> 'Response':
        return cls(b'', HTTPStatus.SEE_OTHER, [('Location', location)])
