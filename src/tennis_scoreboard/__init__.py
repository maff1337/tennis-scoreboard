import logging
from itertools import chain

from waitress import serve

from tennis_scoreboard.bootstrap import build_app
from tennis_scoreboard.config import Settings
from tennis_scoreboard.core.models.base import Base
from tennis_scoreboard.core.models.match import Match
from tennis_scoreboard.core.models.player import Player


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s'
    )

    settings = Settings.from_env()
    app = build_app(settings)

    serve(app, host=settings.host, port=settings.port, threads=settings.threads)
