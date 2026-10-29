import os
from dataclasses import dataclass, field

from tennis_scoreboard.exceptions import ConfigError


@dataclass(frozen=True)
class Settings:
    database_url: str

    host: str = field(default='127.0.0.1')
    port: int = field(default=8080)

    threads: int = field(default=1)

    @classmethod
    def from_env(cls) -> 'Settings':
        try:
            database_url = os.environ['TENNIS_DB_URL']
        except KeyError:
            raise ConfigError(
                'Environment variable TENNIS_DB_URL is not set, e.g. '
                'mysql+pymysql://user:password@localhost/tennis?charset=utf8mb4'
            ) from None

        try:
            port = int(os.environ.get('TENNIS_PORT', cls.port))
            threads = int(os.environ.get('TENNIS_THREADS', cls.threads))
        except ValueError:
            raise ConfigError(
                'TENNIS_PORT and TENNIS_THREADS must be integers'
            ) from None

        return cls(
            database_url=database_url,
            host=os.environ.get('TENNIS_HOST', cls.host),
            port=port,
            threads=threads
        )
