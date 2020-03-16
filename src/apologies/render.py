# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=line-too-long

"""
Render a game on the terminal, for development purposes.
"""

# This is kind of ugly.  It was built by hand and all of the mappings, etc. are
# hardcoded.  Since it's intended as a development and debugging tool, I don't
# really care too much about how nice it looks or how generalizable it is.

# Note: indexes into the rendered board output aren't easily predictible,
# because of the variable length of terminal formatting characters

from .game import RED, BLUE, YELLOW, GREEN

# ANSI terminal escapes for colors
# See also: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#256-colors
_FG_BLACK = "\u001b[30;1m"
_FG_RED = "\u001b[31;1m"
_FG_GREEN = "\u001b[32;1m"
_FG_YELLOW = "\u001b[33;1m"
_FG_BLUE = "\u001b[34;1m"
_FG_MAGENTA = "\u001b[35;1m"
_FG_CYAN = "\u001b[36;1m"
_FG_WHITE = "\u001b[37;1m"
_BG_BLACK = "\u001b[40m"
_BG_RED = "\u001b[41m"
_BG_GREEN = "\u001b[42m"
_BG_YELLOW = "\u001b[43m"
_BG_BLUE = "\u001b[44m"
_BG_MAGENTA = "\u001b[45m"
_BG_CYAN = "\u001b[46m"
_BG_WHITE = "\u001b[47m"
_RESET_COLORS = "\u001b[0m"

# Index into _BOARD_TEXT where a pawn can be placed into a specific square
# Squares are numbered from starting from the upper left, in a clockwise direction
# Only a single pawn can occupy a square
# fmt: off
_SQUARE = [ 
    323, 340, 345, 350, 355, 372, 377, 382, 387, 404, 409, 414, 419, 424, 441, 446, 
    980, 1534, 2088, 2625, 3145, 3631, 4117, 4603, 5089, 5575, 6112, 6649, 7203, 7774, 8288, 8271, 
    8266, 8261, 8256, 8239, 8234, 8229, 8224, 8207, 8202, 8197, 8192, 8187, 8170, 8165, 7631, 7077, 
    6523, 5986, 5466, 4980, 4494, 4008, 3522, 3036, 2499, 1962, 1408, 837,
]
# fmt: on

# Player names as displayed on the board
_PLAYER = {}
_PLAYER[RED] = "r"
_PLAYER[BLUE] = "b"
_PLAYER[YELLOW] = "y"
_PLAYER[GREEN] = "g"

# Indexes in _BOARD_TEXT where a pawn can be placed into a start location, for each player
# There are 4 arbitrary spaces for each of the 4 available pawns
_START = {}
_START[RED] = [1281, 1283, 1285, 1287]
_START[BLUE] = [2416, 2418, 2420, 2422]
_START[YELLOW] = [7145, 7147, 7149, 7151]
_START[GREEN] = [6010, 6012, 6014, 6016]

# Indexes in _BOARD_TEXT where a pawn can be placed into a safe location, for each player
# There are 5 safe squares per color; only a single pawn can occupy a safe square
_SAFE = {}
_SAFE[RED] = [864, 1435, 1989, 2526, 3063]
_SAFE[BLUE] = [1529, 1524, 1519, 1514, 1509]
_SAFE[YELLOW] = [7747, 7176, 6622, 6085, 5548]
_SAFE[GREEN] = [7082, 7087, 7092, 7097, 7102]

# Indexes in _BOARD_TEXT where a pawn can be placed into a home location, for each player
# There are 4 arbitrary home spaces for the 4 available pawns per player
_HOME = {}
_HOME[RED] = [3708, 3710, 3712, 3714]
_HOME[BLUE] = [1318, 1320, 1322, 1324]
_HOME[YELLOW] = [4735, 4737, 4739, 4741]
_HOME[GREEN] = [7108, 7110, 7112, 7114]

# Hardcoded representation of the board, with {} placeholders for color formatting (applied below)
# The board layout was built by hand and then the formatting was placed into it by hand
_BOARD_TEXT = """{}{}{}
{}{}      0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15{}
{}{}    {}{}┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐{}{}   {}
{}{}    {}{}│   │{}{}| ▶ || ◼ || ◼ || ● |{}{}|   ||   ||   ||   |{}{}| ▶ || ◼ || ◼ || ◼ || ● |{}{}|   ||   |{}{}   {}
{}{}    {}{}└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘└───┘{}{}└───┘└───┘{}{}   {}
{}{}    {}{}┌───┐{}     {}{}┌───┐{}                                                            {}{}┌───┐{}{}   {}
{}{} 59 {}{}│   │{}   {}0 {}│   │{}  {}{}┌───────────┐{}       {}{}┌───────────┐{}                         {}{}| ▼ |{}{} 16{}
{}{}    {}{}└───┘{}     {}{}└───┘{}  {}{}│ S T A R T │{}       {}{}│  H O M E  │{}  4    3    2    1    0  {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{}     {}{}┌───┐{}  {}{}│           │{}       {}{}│           │┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐{}{}   {}
{}{} 58 {}{}│ ● │{}   1 {}{}│   │{}  {}{}│  - - - -  │{}       {}{}│  - - - -  │|   ||   ||   ||   ||   || ◼ |{}{} 17{}
{}{}    {}{}└───┘{}     {}{}└───┘{}  {}{}│  0 1 2 3  │{}       {}{}│  0 1 2 3  │└───┘└───┘└───┘└───┘└───┘└───┘{}{}   {}
{}{}    {}{}┌───┐{}     {}{}┌───┐{}  {}{}└───────────┘{}       {}{}└───────────┘{}                         {}{}┌───┐{}{}   {}
{}{} 57 {}{}│ ◼ │{}   2 {}{}│   │{}                                              {}{}┌───────────┐{} {}{}| ◼ |{}{} 18{}
{}{}    {}{}└───┘{}     {}{}└───┘{}                                              {}{}│ S T A R T │{} {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{}     {}{}┌───┐{}                                              {}{}│           │{} {}{}┌───┐{}{}   {}
{}{} 56 {}{}│ ◼ │{}   3 {}{}│   │{}                                              {}{}│  - - - -  │{} {}{}| ● |{}{} 19{}
{}{}    {}{}└───┘{}     {}{}└───┘{}                                              {}{}│  0 1 2 3  │{} {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{}     {}{}┌───┐{}                                              {}{}└───────────┘{} {}{}┌───┐{}{}   {}
{}{} 55 {}{}│ ◼ │{}   4 {}{}│   │{}                                                            {}{}|   |{}{} 19{}
{}{}    {}{}└───┘{}     {}{}└───┘{}                                                            {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{} {}{}┌───────────┐{}                                                        {}{}┌───┐{}{}   {}
{}{} 54 {}{}│ ▲ │{} {}{}│  H O M E  │{}                                                        {}{}|   |{}{} 20{}
{}{}    {}{}└───┘{} {}{}│           │{}                                                        {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{} {}{}│  - - - -  │{}                                                        {}{}┌───┐{}{}   {}
{}{} 53 {}{}│   │{} {}{}│  0 1 2 3  │{}                                                        {}{}|   |{}{} 21{}
{}{}    {}{}└───┘{} {}{}└───────────┘{}                                                        {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{}                                                        {}{}┌───────────┐{} {}{}┌───┐{}{}   {}
{}{} 52 {}{}│   │{}                                                        {}{}│  H O M E  │{} {}{}|   |{}{} 23{}
{}{}    {}{}└───┘{}                                                        {}{}│           │{} {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{}                                                        {}{}│  - - - -  │{} {}{}┌───┐{}{}   {}
{}{} 51 {}{}│   │{}                                                        {}{}│  0 1 2 3  │{} {}{}| ▼ |{}{} 24{}
{}{}    {}{}└───┘{}                                                        {}{}└───────────┘{} {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{}                                                            {}{}┌───┐{}     {}{}┌───┐{}{}   {}
{}{} 50 {}{}│   │{}                                                            {}{}│   │{} 4   {}{}| ◼ |{}{} 25{}
{}{}    {}{}└───┘{} {}{}┌───────────┐{}                                              {}{}└───┘{}     {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{} {}{}│ S T A R T │{}                                              {}{}┌───┐{}     {}{}┌───┐{}{}   {}
{}{} 49 {}{}│ ● │{} {}{}│           │{}                                              {}{}│   │{} 3   {}{}| ◼ |{}{} 26{}
{}{}    {}{}└───┘{} {}{}│  - - - -  │{}                                              {}{}└───┘{}     {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{} {}{}│  0 1 2 3  │{}                                              {}{}┌───┐{}     {}{}┌───┐{}{}   {}
{}{} 48 {}{}│ ◼ │{} {}{}└───────────┘{}                                              {}{}│   │{} 2   {}{}| ◼ |{}{} 27{}
{}{}    {}{}└───┘{}                         {}{}┌───────────┐{}       {}{}┌───────────┐{}  {}{}└───┘{}     {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐│  H O M E  │{}       {}{}│ S T A R T │{}  {}{}┌───┐{}     {}{}┌───┐{}{}   {}
{}{} 47 {}{}│ ◼ │|   ||   ||   ||   ||   |│           │{}       {}{}│           │{}  {}{}│   │{} 1   {}{}| ● |{}{} 28{}
{}{}    {}{}└───┘└───┘└───┘└───┘└───┘└───┘│  - - - -  │{}       {}{}│  - - - -  │{}  {}{}└───┘{}     {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐{}  0    1    2    3    4 {}{} │  0 1 2 3  │{}       {}{}│  0 1 2 3  │{}  {}{}┌───┐{}     {}{}┌───┐{}{}   {}
{}{} 46 {}{}│ ▲ │{}                         {}{}└───────────┘{}       {}{}└───────────┘{}  {}{}│   │{} 0   {}{}|   |{}{} 29{}
{}{}    {}{}└───┘{}                                                            {}{}└───┘{}     {}{}└───┘{}{}   {}
{}{}    {}{}┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐{}{}   {}
{}{}    {}{}│   │|   |{}{}| ● || ◼ || ◼ || ◼ || ◀ |{}{}|   ||   ||   ||   |{}{}| ● || ◼ || ◼ || ◀ |{}{}|   |{}{}   {}
{}{}    {}{}└───┘└───┘{}{}└───┘└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘{}{}   {}
{}{}      45   44   43   42   41   40   39   38   37   36   35   34   33   32   31   30{}
{}{}{}"""

# Color formatting, one entry for each {} placeholder in _BOARD_TEXT
# fmt: off
_BOARD_COLORS = [
    _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_RED, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_RED, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_RED, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_RED, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_RED, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_RED, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _FG_WHITE, _BG_RED, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_RED, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_BLUE, _FG_WHITE, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_GREEN, _FG_WHITE, _BG_CYAN, _BG_YELLOW, _FG_WHITE, _BG_CYAN, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_YELLOW, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_YELLOW, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_YELLOW, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_YELLOW, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_YELLOW, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_YELLOW, _FG_WHITE, _BG_WHITE, _FG_BLACK, _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _RESET_COLORS,
    _BG_BLACK, _FG_WHITE, _RESET_COLORS,
]
# fmt: on


def _generate_empty_board():
    """
    Generate an empty board.
    """
    return "%s\n" % _BOARD_TEXT.format(*_BOARD_COLORS)


def _apply_game_state(board, game):
    """
    Apply game state to a board.
    """
    for player in game.players:
        for pawn in player.pawns:
            if pawn.start:
                index = _START[pawn.color][pawn.index]
            elif pawn.home:
                index = _HOME[pawn.color][pawn.index]
            elif pawn.safe is not None:
                index = _SAFE[pawn.color][pawn.safe]
            elif pawn.square is not None:
                index = _SQUARE[pawn.square]
            else:
                raise ValueError("Pawn is not in a valid state")
            board = board[:index] + _PLAYER[pawn.color] + board[index + 1 :]
    return board


def render_board(game):
    """
    Render the state of a game, returning the board for display.
    
    Args:
        game(Game): The game to render

    Returns:
        str: The board as a string for display on a terminal, including ANSI color escape sequences
    """
    return _apply_game_state(_generate_empty_board(), game)
