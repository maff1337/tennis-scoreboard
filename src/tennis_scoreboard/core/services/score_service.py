from tennis_scoreboard.core.models.match import Match


class ScoreService:
    def __call__(self, match_: Match, player_name: str) -> None:
        if match_.winner is not None:
            raise MatchAlreadyFinishedError('Cannot process finished match')

        match_.score = deepcopy(match_.score)

        self._point_won_by(match_, player_name)

        first_name = match_.first_player.name
        second_name = match_.second_player.name

        first_points = match_.score.points.first_player
        second_points = match_.score.points.second_player

        points_diff = first_points - second_points

        tie_break = (
            match_.score.games.first_player == 6
            and match_.score.games.second_player == 6
        )

        if tie_break:
            if first_points >= 7 and points_diff >= 2:
                self._set_won_by(match_, first_name)
            elif second_points >= 7 and points_diff <= -2:
                self._set_won_by(match_, second_name)
        else:
            if first_points >= 4 and points_diff >= 2:
                self._game_won_by(match_, first_name)
            elif second_points >= 4 and points_diff <= -2:
                self._game_won_by(match_, second_name)

        first_games = match_.score.games.first_player
        second_games = match_.score.games.second_player

        games_diff = first_games - second_games

        if not tie_break:
            if first_games >= 6 and games_diff >= 2:
                self._set_won_by(match_, first_name)
            elif second_games >= 6 and games_diff <= -2:
                self._set_won_by(match_, second_name)

        first_sets = match_.score.sets.first_player
        second_sets = match_.score.sets.second_player

        if first_sets == 2:
            self._match_won_by(match_, first_name)
        elif second_sets == 2:
            self._match_won_by(match_, second_name)

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
