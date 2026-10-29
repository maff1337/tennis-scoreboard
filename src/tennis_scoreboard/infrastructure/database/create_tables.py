from tennis_scoreboard.config import Settings
from tennis_scoreboard.core.models.base import Base
from tennis_scoreboard.infrastructure.database.engine import create_db_engine


def main() -> None:
    engine = create_db_engine(Settings.from_env().database_url)
    Base.metadata.create_all(engine)
    print('Tables created')


if __name__ == '__main__':
    main()
