import pytest

from tennis_scoreboard.core.models.match import Match
from tennis_scoreboard.core.models.player import Player
from tennis_scoreboard.core.services.score_service import ScoreService
from tennis_scoreboard.core.vo.score import Score


@pytest.fixture
def players() -> tuple[Player, Player]:
    return (
        Player(id=1, name='First'),
        Player(id=2, name='Second'),
    )


@pytest.fixture
def match_(players: tuple[Player, Player]) -> Match:
    first, second = players

    return Match(first_player=first, second_player=second, score=Score())


@pytest.fixture
def service() -> ScoreService:
    return ScoreService()


@pytest.mark.parametrize(
    ('player_name', 'expected_first', 'expected_second'),
    [
        ('First', 1, 0),
        ('Second', 0, 1)
    ]
)
def test_award_points(
    service: ScoreService,
    match_: Match,
    player_name: str,
    expected_first: int,
    expected_second: int
) -> None:
    service(match_, player_name)

    assert match_.score.points.first_player == expected_first
    assert match_.score.points.second_player == expected_second


def test_game_won_by_first_player(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.points.first_player = 3

    service(match_, 'First')

    assert match_.score.games.first_player == 1
    assert match_.score.games.second_player == 0
    assert match_.score.points.first_player == 0
    assert match_.score.points.second_player == 0


def test_opponents_returns_score_to_deuce(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.points.first_player = 4
    match_.score.points.second_player = 3

    service(match_, 'Second')

    assert match_.score.points.first_player == 4
    assert match_.score.points.second_player == 4
    assert match_.score.games.first_player == 0
    assert match_.score.games.second_player == 0


def test_set_won_by_first_player(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.games.first_player = 5
    match_.score.games.second_player = 4
    match_.score.points.first_player = 3
    match_.score.points.second_player = 2

    service(match_, 'First')

    assert match_.score.sets.first_player == 1
    assert match_.score.sets.second_player == 0
    assert match_.score.games.first_player == 0
    assert match_.score.games.second_player == 0
    assert match_.score.points.first_player == 0
    assert match_.score.points.second_player == 0


def test_match_won_by_first_player(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.sets.first_player = 1
    match_.score.games.first_player = 5
    match_.score.games.second_player = 4
    match_.score.points.first_player = 6
    match_.score.points.second_player = 5

    service(match_, 'First')

    assert match_.score.sets.first_player == 2
    assert match_.winner is match_.first_player


def test_tiebreak_won_by_first_player(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.games.first_player = 6
    match_.score.games.second_player = 6
    match_.score.points.first_player = 6
    match_.score.points.second_player = 6

    service(match_, 'First')
    service(match_, 'First')

    assert match_.score.sets.first_player == 1
    assert match_.score.games.first_player == 0
    assert match_.score.games.second_player == 0
    assert match_.score.points.first_player == 0
    assert match_.score.points.second_player == 0


def test_unknown_player_raises_exception(
    service: ScoreService,
    match_: Match
) -> None:
    with pytest.raises(Exception):
        service(match_, "Unknown")

    assert match_.score.points.first_player == 0
    assert match_.score.points.second_player == 0


def test_cannot_score_after_match_finished(
    service: ScoreService,
    match_: Match
) -> None:
    match_.winner = match_.first_player

    with pytest.raises(Exception):
        service(match_, 'First')

    assert match_.score.points.first_player == 0


def test_tiebreak_at_7_6_does_not_finish_set(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.games.first_player = 6
    match_.score.games.second_player = 6
    match_.score.points.first_player = 6
    match_.score.points.second_player = 6

    service(match_, 'First')

    assert match_.score.sets.first_player == 0
    assert match_.score.games.first_player == 6
    assert match_.score.games.second_player == 6
    assert match_.score.points.first_player == 7
    assert match_.score.points.second_player == 6


def test_tiebreak_at_8_7_does_not_finish_set(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.games.first_player = 6
    match_.score.games.second_player = 6
    match_.score.points.first_player = 7
    match_.score.points.second_player = 7

    service(match_, 'First')

    assert match_.score.sets.first_player == 0
    assert match_.score.games.first_player == 6
    assert match_.score.games.second_player == 6
    assert match_.score.points.first_player == 8
    assert match_.score.points.second_player == 7


def test_tiebreak_at_8_6_finish_set(
    service: ScoreService,
    match_: Match
) -> None:
    match_.score.games.first_player = 6
    match_.score.games.second_player = 6
    match_.score.points.first_player = 7
    match_.score.points.second_player = 6

    service(match_, 'First')

    assert match_.score.sets.first_player == 1
    assert match_.score.games.first_player == 0
    assert match_.score.games.second_player == 0
    assert match_.score.points.first_player == 0
    assert match_.score.points.second_player == 0


def test_tiebreak_does_not_use_regular_game_scoring(
    service: ScoreService,
    match_: Match,
) -> None:
    match_.score.games.first_player = 6
    match_.score.games.second_player = 6
    match_.score.points.first_player = 3
    match_.score.points.second_player = 0

    service(match_, "First")

    assert match_.score.points.first_player == 4
    assert match_.score.points.second_player == 0
    assert match_.score.games.first_player == 6
    assert match_.score.games.second_player == 6
    assert match_.score.sets.first_player == 0
    assert match_.score.sets.second_player == 0
