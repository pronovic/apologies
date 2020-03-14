# -*- coding: utf-8 -*-
# vim: set ft=python ts=3 sw=3 expandtab: 
# pylint: disable=line-too-long
# Render a game on the terminal, for development purposes

# This is kind of ugly.  It was built by hand and all of the mappings, etc. are
# hardcoded.  Since it's intended as a development and debugging tool, I don't
# really care too much about how nice it looks or how generalizable it is.

# Note: indexes into the rendered board output aren't easily predictible,
# because of the variable length of formatting characters

from .game import RED, BLUE, YELLOW, GREEN

# ANSI terminal escapes for colors
# See also: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#256-colors
FG_BLACK = "\u001b[30;1m"
FG_RED = "\u001b[31;1m"
FG_GREEN = "\u001b[32;1m"
FG_YELLOW = "\u001b[33;1m"
FG_BLUE = "\u001b[34;1m"
FG_MAGENTA = "\u001b[35;1m"
FG_CYAN = "\u001b[36;1m"
FG_WHITE = "\u001b[37;1m"
BG_BLACK = "\u001b[40m"
BG_RED = "\u001b[41m"
BG_GREEN = "\u001b[42m"
BG_YELLOW = "\u001b[43m"
BG_BLUE = "\u001b[44m"
BG_MAGENTA = "\u001b[45m"
BG_CYAN = "\u001b[46m"
BG_WHITE = "\u001b[47m"
RESET_COLORS = "\u001b[0m"

# Index into BOARD_TEXT where a pawn can be placed into a specific square
# Squares are numbered from starting from the upper left, in a clockwise direction
# Only a single pawn can occupy a square
SQUARE = [ 
   323, 340, 345, 350, 355, 372, 377, 382, 387, 404, 409, 414, 419, 424, 441, 446, 
   980, 1534, 2088, 2625, 3145, 3631, 4117, 4603, 5089, 5575, 6112, 6649, 7203, 7774, 8288, 8271, 
   8266, 8261, 8256, 8239, 8234, 8229, 8224, 8207, 8202, 8197, 8192, 8187, 8170, 8165, 7631, 7077, 
   6523, 5986, 5466, 4980, 4494, 4008, 3522, 3036, 2499, 1962, 1408, 837,
]

# Player names as displayed on the board
PLAYER = {}
PLAYER[RED] = "r"
PLAYER[BLUE] = "b"
PLAYER[YELLOW] = "y"
PLAYER[GREEN] = "g"

# Indexes in BOARD_TEXT where a pawn can be placed into a start location, for each player
# There are 4 arbitrary spaces for each of the 4 available pawns
START = {}
START[RED] = [1281, 1283, 1285, 1287,]
START[BLUE] = [2416, 2418, 2420, 2422,]
START[YELLOW] = [7145, 7147, 7149, 7151,]
START[GREEN] = [6010, 6012, 6014, 6016,]

# Indexes in BOARD_TEXT where a pawn can be placed into a safe location, for each player
# There are 5 safe squares per color; only a single pawn can occupy a safe square
SAFE = {}
SAFE[RED] = [864, 1435, 1989, 2526, 3063,]
SAFE[BLUE] = [1529, 1524, 1519, 1514, 1509,]
SAFE[YELLOW] = [7747, 7176, 6622, 6085, 5548,]
SAFE[GREEN] = [7082, 7087, 7092, 7097, 7102,]

# Indexes in BOARD_TEXT where a pawn can be placed into a home location, for each player
# There are 4 arbitrary home spaces for the 4 available pawns per player
HOME = {}
HOME[RED] = [3708, 3710, 3712, 3714,]
HOME[BLUE] = [1318, 1320, 1322, 1324,]
HOME[YELLOW] = [4735, 4737, 4739, 4741,]
HOME[GREEN] = [7108, 7110, 7112, 7114,]

# Hardcoded representation of the board, with {} placeholders for color formatting (applied below)
# The board layout was built by hand and then the formatting was placed into it by hand
BOARD_TEXT = """{}{}{}
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

# Color formatting, one entry for each {} placeholder in BOARD_TEXT
BOARD_COLORS = [
   BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, FG_WHITE, BG_RED, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, RESET_COLORS,
   BG_BLACK, FG_WHITE, RESET_COLORS,
]

# Generate the empty board
def _generate_empty_board():
   return "%s\n" % BOARD_TEXT.format(*BOARD_COLORS)

# Apply the game state onto the empty board
def _apply_game_state(board, game):
   for player in game.players:
      for pawn in player.pawns:
         if pawn.start:
            index = START[pawn.color][pawn.index]
         elif pawn.home:
            index = HOME[pawn.color][pawn.index]
         elif pawn.safe is not None:
            index = SAFE[pawn.color][pawn.safe]
         elif pawn.square is not None:
            index = SQUARE[pawn.square]
         else:
            raise ValueError("Pawn is not in a valid state")
         board = board[:index] + PLAYER[pawn.color] + board[index+1:]
   return board

# Render the state of a game, returning the board for display
def render_board(game):
   return _apply_game_state(_generate_empty_board(), game)
