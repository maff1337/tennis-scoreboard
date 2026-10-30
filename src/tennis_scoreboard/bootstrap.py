from pathlib import Path

from sqlalchemy.orm import sessionmaker

from tennis_scoreboard.application.repositories.repo_factories import (
    MatchRepoFactory,
    PlayerRepoFactory,
)
from tennis_scoreboard.application.uow.uow_factory import UowFactory
from tennis_scoreboard.config import Settings
from tennis_scoreboard.core.services.score_service import ScoreService
from tennis_scoreboard.di import Container
from tennis_scoreboard.infrastructure.database.engine import create_db_engine
from tennis_scoreboard.infrastructure.repositories.sqla_match_repo import SqlaMatchRepo
from tennis_scoreboard.infrastructure.repositories.sqla_player_repo import (
    SqlaPlayerRepo,
)
from tennis_scoreboard.infrastructure.uow.sqla_uow_factory import SqlaUowFactory
from tennis_scoreboard.web.app import Application
from tennis_scoreboard.web.controllers import MatchController
from tennis_scoreboard.web.renderer import TemplateRenderer
from tennis_scoreboard.web.router import Router
from tennis_scoreboard.web.static import StaticFiles

WEB_DIR = Path(__file__).parent / 'web'
TEMPLATES_DIR = WEB_DIR / 'templates'
STATIC_DIR = WEB_DIR / 'static'


def build_container(settings: Settings) -> Container:
    c = Container()

    engine = create_db_engine(settings.database_url)
    c.bind_instance(sessionmaker, sessionmaker(engine, expire_on_commit=False))

    c.bind_instance(PlayerRepoFactory, SqlaPlayerRepo)
    c.bind_instance(MatchRepoFactory, SqlaMatchRepo)

    c.bind(UowFactory, SqlaUowFactory)
    c.bind(ScoreService, ScoreService)
    c.bind_instance(TemplateRenderer, TemplateRenderer(str(TEMPLATES_DIR)))

    return c


def build_app(settings: Settings) -> Application:
    container = build_container(settings)

    controller = container.resolve(MatchController)
    view = container.resolve(TemplateRenderer)

    router = Router()
    router.add('GET', '/', lambda _: view.render('index.html'))
    router.add('GET', '/new-match', controller.new_match_form)
    router.add('POST', '/new-match', controller.create_match)
    router.add('GET', '/match-score', controller.match_score)
    router.add('POST', '/match-score', controller.add_point)
    router.add('GET', '/matches', controller.matches)

    return Application(router, StaticFiles(STATIC_DIR), view.error_page)
