from dataclasses import dataclass, field


@dataclass
class Points:
    first_player: int = field(default=0)
    second_player: int = field(default=0)


@dataclass
class Games:
    first_player: int = field(default=0)
    second_player: int = field(default=0)


@dataclass
class Sets:
    first_player: int = field(default=0)
    second_player: int = field(default=0)


@dataclass
class Score:
    sets: Sets = field(default=Sets())
    games: Games = field(default=Games())
    points: Points = field(default=Points())
