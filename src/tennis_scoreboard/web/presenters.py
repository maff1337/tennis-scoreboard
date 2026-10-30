from tennis_scoreboard.core.vo.score import Score

_STEPS = ('0', '15', '30', '40')


def render_points(score: Score) -> tuple[str, str]:
    first = score.points.first_player
    second = score.points.second_player

    if score.games.first_player == 6 and score.games.second_player == 6:
        return str(first), str(second)

    if first >= 3 and second >= 3:
        if first == second:
            return '40', '40'
        return ('Ad', '40') if first > second else ('40', 'Ad')

    return _STEPS[min(first, 3)], _STEPS[min(second, 3)]
