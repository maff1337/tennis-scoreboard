from sqlalchemy.orm.attributes import flag_modified

from tennis_scoreboard.core.models.match import Match
from tennis_scoreboard.exceptions import (
    MatchAlreadyFinishedError,
    PlayerNotInMatchError,
)


class ScoreService:
    SETS_TO_WIN = 2
    GAMES_TO_WIN_SET = 6
    TIE_BREAK_AT_GAMES = 6
    POINTS_TO_WIN_GAME = 4
    POINTS_TO_WIN_TIE_BREAK = 7
    MIN_LEAD = 2

    def __call__(self, match_: Match, player_name: str) -> None:
        if match_.winner is not None:
            raise MatchAlreadyFinishedError('Cannot process finished match')

        self._point_won_by(match_, player_name)

        first_name = match_.first_player.name
        second_name = match_.second_player.name

        first_points = match_.score.points.first_player
        second_points = match_.score.points.second_player

        points_diff = first_points - second_points

        tie_break = (
            match_.score.games.first_player == self.TIE_BREAK_AT_GAMES
            and match_.score.games.second_player == self.TIE_BREAK_AT_GAMES
        )

        if tie_break:
            if (first_points >= self.POINTS_TO_WIN_TIE_BREAK
                    and points_diff >= self.MIN_LEAD):
                self._set_won_by(match_, first_name)
            elif (second_points >= self.POINTS_TO_WIN_TIE_BREAK
                  and points_diff <= -self.MIN_LEAD):
                self._set_won_by(match_, second_name)
        else:
            if (first_points >= self.POINTS_TO_WIN_GAME
                    and points_diff >= self.MIN_LEAD):
                self._game_won_by(match_, first_name)
            elif (second_points >= self.POINTS_TO_WIN_GAME
                  and points_diff <= -self.MIN_LEAD):
                self._game_won_by(match_, second_name)

        first_games = match_.score.games.first_player
        second_games = match_.score.games.second_player

        games_diff = first_games - second_games

        if not tie_break:
            if (first_games >= self.GAMES_TO_WIN_SET
                    and games_diff >= self.MIN_LEAD):
                self._set_won_by(match_, first_name)
            elif (second_games >= self.GAMES_TO_WIN_SET
                  and games_diff <= -self.MIN_LEAD):
                self._set_won_by(match_, second_name)

        first_sets = match_.score.sets.first_player
        second_sets = match_.score.sets.second_player

        if first_sets == self.SETS_TO_WIN:
            self._match_won_by(match_, first_name)
        elif second_sets == self.SETS_TO_WIN:
            self._match_won_by(match_, second_name)

        flag_modified(match_, 'score')

    def _point_won_by(self, match_: Match, player_name: str) -> None:
        if player_name == match_.first_player.name:
            match_.score.points.first_player += 1
        elif player_name == match_.second_player.name:
            match_.score.points.second_player += 1
        else:
            raise PlayerNotInMatchError(
                f'Player {player_name} is not participating in this match')

    def _game_won_by(self, match_: Match, player_name: str) -> None:
        if player_name == match_.first_player.name:
            match_.score.games.first_player += 1
        elif player_name == match_.second_player.name:
            match_.score.games.second_player += 1
        else:
            raise PlayerNotInMatchError(
                f'Player {player_name} is not participating in this match')

        match_.score.points.first_player = 0
        match_.score.points.second_player = 0

    def _set_won_by(self, match_: Match, player_name: str) -> None:
        if player_name == match_.first_player.name:
            match_.score.sets.first_player += 1
        elif player_name == match_.second_player.name:
            match_.score.sets.second_player += 1
        else:
            raise PlayerNotInMatchError(
                f'Player {player_name} is not participating in this match')

        match_.score.games.first_player = 0
        match_.score.games.second_player = 0

        match_.score.points.first_player = 0
        match_.score.points.second_player = 0

    def _match_won_by(self, match_: Match, player_name: str) -> None:
        if player_name == match_.first_player.name:
            match_.winner = match_.first_player
        elif player_name == match_.second_player.name:
            match_.winner = match_.second_player
        else:
            raise PlayerNotInMatchError(
                f'Player {player_name} is not participating in this match')
