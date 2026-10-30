from http import HTTPStatus


class PlayerValidationError(Exception):
    ...


class MatchAlreadyFinishedError(Exception):
    ...


class PlayerNotInMatchError(Exception):
    ...


class MatchNotFoundError(Exception):
    ...


class SamePlayersError(Exception):
    ...


class DIError(Exception):
    ...


class ConfigError(Exception):
    ...


class HttpError(Exception):
    def __init__(self, status: HTTPStatus, message: str = '') -> None:
        super().__init__(message or status.phrase)
        self.status = status
