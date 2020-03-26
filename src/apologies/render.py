# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=line-too-long

"""
Render a game as a string.
"""

# This is kind of ugly.  It was built by hand and all of the mappings, etc. are
# hardcoded.  Since it's intended as a development and debugging tool, I don't
# really care too much about how nice it looks or how generalizable it is.

# Note: indexes into the rendered board output aren't easily predictible,
# because of the variable length of terminal formatting characters

from .game import Game, PlayerColor

# Index into _BOARD_TEXT where a pawn can be placed into a specific square
# Squares are numbered from starting from the upper left, in a clockwise direction
# Only a single pawn can occupy a square
# fmt: off
_SQUARE = [
    177, 182, 187, 192, 197, 202, 207, 212, 217, 222, 227, 232, 237, 242, 247, 252,
    507, 765, 1023, 1281, 1539, 1797, 2055, 2313, 2571, 2829, 3087, 3345, 3603, 3861,
    4119, 4114, 4109, 4104, 4099, 4094, 4089, 4084, 4079, 4074, 4069, 4064, 4059, 4054, 4049, 4044,
    3786, 3528, 3270, 3012, 2754, 2496, 2238, 1980, 1722, 1464, 1206, 948, 690, 432,
]
# fmt: on

# Player names as displayed on the board
# noinspection PyDictCreation
_PLAYER = {}
_PLAYER[PlayerColor.RED] = "r"
_PLAYER[PlayerColor.BLUE] = "b"
_PLAYER[PlayerColor.YELLOW] = "y"
_PLAYER[PlayerColor.GREEN] = "g"

# Indexes in _BOARD_TEXT where a pawn can be placed into a start location, for each player
# There are 4 arbitrary spaces for each of the 4 available pawns
# noinspection PyDictCreation
_START = {}
_START[PlayerColor.RED] = [623, 625, 627, 629]
_START[PlayerColor.BLUE] = [1183, 1185, 1187, 1189]
_START[PlayerColor.YELLOW] = [3579, 3581, 3583, 3585]
_START[PlayerColor.GREEN] = [3019, 3021, 3023, 3025]

# Indexes in _BOARD_TEXT where a pawn can be placed into a safe location, for each player
# There are 5 safe squares per color; only a single pawn can occupy a safe square
# noinspection PyDictCreation
_SAFE = {}
_SAFE[PlayerColor.RED] = [442, 700, 958, 1216, 1474]
_SAFE[PlayerColor.BLUE] = [760, 755, 750, 745, 740]
_SAFE[PlayerColor.YELLOW] = [3851, 3593, 3335, 3077, 2819]
_SAFE[PlayerColor.GREEN] = [3533, 3538, 3543, 3548, 3553]

# Indexes in _BOARD_TEXT where a pawn can be placed into a home location, for each player
# There are 4 arbitrary home spaces for the 4 available pawns per player
# noinspection PyDictCreation
_HOME = {}
_HOME[PlayerColor.RED] = [1817, 1819, 1821, 1823]
_HOME[PlayerColor.BLUE] = [643, 645, 647, 649]
_HOME[PlayerColor.YELLOW] = [2388, 2390, 2392, 2394]
_HOME[PlayerColor.GREEN] = [3559, 3561, 3563, 3565]

# Hardcoded representation of the board, built by hand
_BOARD_TEXT = """

      0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
    ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐
    │   │| ▶ || ◼ || ◼ || ● ||   ||   ||   ||   || ▶ || ◼ || ◼ || ◼ || ● ||   ||   |
    └───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘
    ┌───┐     ┌───┐                                                            ┌───┐
 59 │   │   0 │   │  ┌───────────┐       ┌───────────┐                         | ▼ | 16
    └───┘     └───┘  │ S T A R T │       │  H O M E  │  4    3    2    1    0  └───┘
    ┌───┐     ┌───┐  │           │       │           │┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐
 58 │ ● │   1 │   │  │  - - - -  │       │  - - - -  │|   ||   ||   ||   ||   || ◼ | 17
    └───┘     └───┘  │  0 1 2 3  │       │  0 1 2 3  │└───┘└───┘└───┘└───┘└───┘└───┘
    ┌───┐     ┌───┐  └───────────┘       └───────────┘                         ┌───┐
 57 │ ◼ │   2 │   │                                              ┌───────────┐ | ◼ | 18
    └───┘     └───┘                                              │ S T A R T │ └───┘
    ┌───┐     ┌───┐                                              │           │ ┌───┐
 56 │ ◼ │   3 │   │                                              │  - - - -  │ | ● | 19
    └───┘     └───┘                                              │  0 1 2 3  │ └───┘
    ┌───┐     ┌───┐                                              └───────────┘ ┌───┐
 55 │ ◼ │   4 │   │                                                            |   | 20
    └───┘     └───┘                                                            └───┘
    ┌───┐ ┌───────────┐                                                        ┌───┐
 54 │ ▲ │ │  H O M E  │                                                        |   | 21
    └───┘ │           │                                                        └───┘
    ┌───┐ │  - - - -  │                                                        ┌───┐
 53 │   │ │  0 1 2 3  │                                                        |   | 22
    └───┘ └───────────┘                                                        └───┘
    ┌───┐                                                        ┌───────────┐ ┌───┐
 52 │   │                                                        │  H O M E  │ |   | 23
    └───┘                                                        │           │ └───┘
    ┌───┐                                                        │  - - - -  │ ┌───┐
 51 │   │                                                        │  0 1 2 3  │ | ▼ | 24
    └───┘                                                        └───────────┘ └───┘
    ┌───┐                                                            ┌───┐     ┌───┐
 50 │   │                                                            │   │ 4   | ◼ | 25
    └───┘ ┌───────────┐                                              └───┘     └───┘
    ┌───┐ │ S T A R T │                                              ┌───┐     ┌───┐
 49 │ ● │ │           │                                              │   │ 3   | ◼ | 26
    └───┘ │  - - - -  │                                              └───┘     └───┘
    ┌───┐ │  0 1 2 3  │                                              ┌───┐     ┌───┐
 48 │ ◼ │ └───────────┘                                              │   │ 2   | ◼ | 27
    └───┘                         ┌───────────┐       ┌───────────┐  └───┘     └───┘
    ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐│  H O M E  │       │ S T A R T │  ┌───┐     ┌───┐
 47 │ ◼ │|   ||   ||   ||   ||   |│           │       │           │  │   │ 1   | ● | 28
    └───┘└───┘└───┘└───┘└───┘└───┘│  - - - -  │       │  - - - -  │  └───┘     └───┘
    ┌───┐  0    1    2    3    4  │  0 1 2 3  │       │  0 1 2 3  │  ┌───┐     ┌───┐
 46 │ ▲ │                         └───────────┘       └───────────┘  │   │ 0   |   | 29
    └───┘                                                            └───┘     └───┘
    ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐
    │   │|   || ● || ◼ || ◼ || ◼ || ◀ ||   ||   ||   ||   || ● || ◼ || ◼ || ◀ ||   | 
    └───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘
      45   44   43   42   41   40   39   38   37   36   35   34   33   32   31   30

"""


def _apply_game_state(board: str, game: Game) -> str:
    """
    Apply game state to a board.
    """
    for player in game.players.values():
        for pawn in player.pawns:
            if pawn.position.start:
                index = _START[pawn.color][pawn.index]
            elif pawn.position.home:
                index = _HOME[pawn.color][pawn.index]
            elif pawn.position.safe is not None:
                index = _SAFE[pawn.color][pawn.position.safe]
            elif pawn.position.square is not None:
                index = _SQUARE[pawn.position.square]
            else:
                raise ValueError("Pawn is not in a valid state")
            board = board[:index] + _PLAYER[pawn.color] + board[index + 1 :]
    return board


def render_board(game: Game) -> str:
    """
    Render the state of a game, returning the board for display.

    Args:
        game(Game): The game to render

    Returns:
        str: The board as a string, to be printed or for display on a terminal
    """
    return _apply_game_state(_BOARD_TEXT, game)
