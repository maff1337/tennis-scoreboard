# Tennis Scoreboard

Web application for keeping score of tennis matches.

## Stack

- `Python 3.13+`
- `MariaDB`
- `SQLAlchemy`
- `Waitress` (WSGI, no web framework)
- `Jinja2`
- `uv`

## Features

- Create a match, players are added automatically
- Point-by-point scoring: games, sets, tie-break
- Match list with pagination and search by player name
- Final score page for finished matches

## Run

Create the database and the user (once):

```sql
CREATE DATABASE tennis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tennis'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON tennis.* TO 'tennis'@'localhost';
```

Then:

```bash
uv sync
export TENNIS_DB_URL='mysql+pymysql://tennis:your_password@localhost/tennis?charset=utf8mb4'
uv run python -m tennis_scoreboard.infrastructure.database.create_tables
uv run tennis
```

The app is available at http://localhost:8080.

License - MIT