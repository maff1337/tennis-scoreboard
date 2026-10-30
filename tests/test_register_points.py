from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tennis_scoreboard.application.use_cases.create_match import CreateMatchUseCase
from tennis_scoreboard.application.use_cases.get_match_score import GetMatchScoreUseCase
from tennis_scoreboard.application.use_cases.register_point import RegisterPointUseCase
from tennis_scoreboard.core.models.base import Base
from tennis_scoreboard.core.services.score_service import ScoreService
from tennis_scoreboard.core.vo.score import Points
from tennis_scoreboard.infrastructure.repositories.sqla_match_repo import SqlaMatchRepo
from tennis_scoreboard.infrastructure.repositories.sqla_player_repo import (
    SqlaPlayerRepo,
)
from tennis_scoreboard.infrastructure.uow.sqla_uow_factory import SqlaUowFactory


def test_point_is_persisted() -> None:
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    uow_factory = SqlaUowFactory(
        sessionmaker(
            engine, expire_on_commit=False), SqlaPlayerRepo, SqlaMatchRepo
    )

    match_uuid = CreateMatchUseCase(uow_factory)('Ivan', 'Petr')
    RegisterPointUseCase(uow_factory, ScoreService())(match_uuid, 'Ivan')

    assert GetMatchScoreUseCase(uow_factory)(
        match_uuid).score.points == Points(1, 0)
