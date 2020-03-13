# -*- coding: utf-8 -*-
# vim: set ft=python ts=3 sw=3 expandtab: 
# Render a game on the terminal, for development purposes

# This is kind of ugly.  It was built by hand and all of the mappings, etc. are
# hardcoded.  Since it's intended as a development and debugging tool, I don't
# really care too much about how nice it looks or how generalizable it is.

# Note: indexes into the rendered board output aren't easily predictible,
# because of the variable length of formatting characters

from game import Game, RED, BLUE, YELLOW, GREEN

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
SQUARE = [ 160, 177, 182, 187, 192, 209, 214, 219, 224, 241, 246, 
           251, 256, 261, 278, 283, 724, 1185, 1646, 2090, 2517, 
           2910, 3303, 3696, 4089, 4482, 4926, 5370, 5831, 6309, 
           6730, 6713, 6708, 6703, 6698, 6681, 6676, 6671, 6666, 
           6649, 6644, 6639, 6634, 6629, 6612, 6607, 6166, 5705, 
           5244, 4800, 4373, 3980, 3587, 3194, 2801, 2408, 1964, 
           1520, 1059, 581, ]

# Player names as displayed on the board
PLAYER = {}
PLAYER[RED] = "r"
PLAYER[BLUE] = "b"
PLAYER[YELLOW] = "y"
PLAYER[GREEN] = "g"

# Indexes in BOARD_TEXT where a pawn can be placed into a start location, for each player
# There are 4 arbitrary spaces for each of the 4 available pawns
START = {}
START[RED] = [ 1111, 1113, 1115, 1117, ]
START[BLUE] = [ 2060, 2062, 2064, 2066, ]
START[YELLOW] = [ 5921, 5923, 5925, 5927, ]
START[GREEN] = [ 4972, 4974, 4976, 4978, ]

# Indexes in BOARD_TEXT where a pawn can be placed into a safe location, for each player
# There are 5 safe squares per color; only a single pawn can occupy a safe square
SAFE = {}
SAFE[RED] = [ 608, 1086, 1547, 1991, 2435, ]
SAFE[BLUE] = [ 1180, 1175, 1170, 1165, 1160, ]
SAFE[YELLOW] = [ 6282, 5804, 5343, 4899, 4455, ]
SAFE[GREEN] = [ 5710, 5715, 5720, 5725, 5730, ]

# Indexes in BOARD_TEXT where a pawn can be placed into a home location, for each player
# There are 4 arbitrary home spaces for the 4 available pawns per player
HOME = {}
HOME[RED] = [ 3086, 3088, 3090, 3092, ]
HOME[BLUE] = [ 1148, 1150, 1152, 1154, ]
HOME[YELLOW] = [ 3928, 3930, 3932, 3934, ]
HOME[GREEN] = [ 5885, 5887, 5889, 5891, ]

# Hardcoded representation of the board, with {} placeholders for color formatting (applied below)
# The board layout was built by hand and then the formatting was placed into it by hand
BOARD_TEXT = """
{}{}┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐{}
{}{}│   │{}{}| ▶ || ◼ || ◼ || ● |{}{}|   ||   ||   ||   |{}{}| ▶ || ◼ || ◼ || ◼ || ● |{}{}|   ||   |{}
{}{}└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘└───┘{}{}└───┘└───┘{}
{}{}┌───┐{}     {}{}┌───┐{}                                                            {}{}┌───┐{}
{}{}│   │{}     {}{}│   │{}  {}{}┌───────────┐{}       {}{}┌───────────┐{}                         {}{}| ▼ |{}
{}{}└───┘{}     {}{}└───┘{}  {}{}│ S T A R T │{}       {}{}│  H O M E  │{}                         {}{}└───┘{}
{}{}┌───┐{}     {}{}┌───┐{}  {}{}│           │{}       {}{}│           │┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐{}
{}{}│ ● │{}     {}{}│   │{}  {}{}│           │{}       {}{}│           │|   ||   ||   ||   ||   || ◼ |{}
{}{}└───┘{}     {}{}└───┘{}  {}{}│           │{}       {}{}│           │└───┘└───┘└───┘└───┘└───┘└───┘{}
{}{}┌───┐{}     {}{}┌───┐{}  {}{}└───────────┘{}       {}{}└───────────┘{}                         {}{}┌───┐{}
{}{}│ ◼ │{}     {}{}│   │{}                                              {}{}┌───────────┐{} {}{}| ◼ |{}
{}{}└───┘{}     {}{}└───┘{}                                              {}{}│ S T A R T │{} {}{}└───┘{}
{}{}┌───┐{}     {}{}┌───┐{}                                              {}{}│           │{} {}{}┌───┐{}
{}{}│ ◼ │{}     {}{}│   │{}                                              {}{}│           │{} {}{}| ● |{}
{}{}└───┘{}     {}{}└───┘{}                                              {}{}│           │{} {}{}└───┘{}
{}{}┌───┐{}     {}{}┌───┐{}                                              {}{}└───────────┘{} {}{}┌───┐{}
{}{}│ ◼ │{}     {}{}│   │{}                                                            {}{}|   |{}
{}{}└───┘{}     {}{}└───┘{}                                                            {}{}└───┘{}
{}{}┌───┐{} {}{}┌───────────┐{}                                                        {}{}┌───┐{}
{}{}│ ▲ │{} {}{}│  H O M E  │{}                                                        {}{}|   |{}
{}{}└───┘{} {}{}│           │{}                                                        {}{}└───┘{}
{}{}┌───┐{} {}{}│           │{}                                                        {}{}┌───┐{}
{}{}│   │{} {}{}│           │{}                                                        {}{}|   |{}
{}{}└───┘{} {}{}└───────────┘{}                                                        {}{}└───┘{}
{}{}┌───┐{}                                                        {}{}┌───────────┐{} {}{}┌───┐{}
{}{}│   │{}                                                        {}{}│  H O M E  │{} {}{}|   |{}
{}{}└───┘{}                                                        {}{}│           │{} {}{}└───┘{}
{}{}┌───┐{}                                                        {}{}│           │{} {}{}┌───┐{}
{}{}│   │{}                                                        {}{}│           │{} {}{}| ▼ |{}
{}{}└───┘{}                                                        {}{}└───────────┘{} {}{}└───┘{}
{}{}┌───┐{}                                                            {}{}┌───┐{}     {}{}┌───┐{}
{}{}│   │{}                                                            {}{}│   │{}     {}{}| ◼ |{}
{}{}└───┘{} {}{}┌───────────┐{}                                              {}{}└───┘{}     {}{}└───┘{}
{}{}┌───┐{} {}{}│ S T A R T │{}                                              {}{}┌───┐{}     {}{}┌───┐{}
{}{}│ ● │{} {}{}│           │{}                                              {}{}│   │{}     {}{}| ◼ |{}
{}{}└───┘{} {}{}│           │{}                                              {}{}└───┘{}     {}{}└───┘{}
{}{}┌───┐{} {}{}│           │{}                                              {}{}┌───┐{}     {}{}┌───┐{}
{}{}│ ◼ │{} {}{}└───────────┘{}                                              {}{}│   │{}     {}{}| ◼ |{}
{}{}└───┘{}                         {}{}┌───────────┐{}       {}{}┌───────────┐{}  {}{}└───┘{}     {}{}└───┘{}
{}{}┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐│  H O M E  │{}       {}{}│ S T A R T │{}  {}{}┌───┐{}     {}{}┌───┐{}
{}{}│ ◼ │|   ||   ||   ||   ||   |│           │{}       {}{}│           │{}  {}{}│   │{}     {}{}| ● |{}
{}{}└───┘└───┘└───┘└───┘└───┘└───┘│           │{}       {}{}│           │{}  {}{}└───┘{}     {}{}└───┘{}
{}{}┌───┐{}                        {}{} │           │{}       {}{}│           │{}  {}{}┌───┐{}     {}{}┌───┐{}
{}{}│ ▲ │{}                         {}{}└───────────┘{}       {}{}└───────────┘{}  {}{}│   │{}     {}{}|   |{}
{}{}└───┘{}                                                            {}{}└───┘{}     {}{}└───┘{}
{}{}┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐┌───┐┌───┐┌───┐{}{}┌───┐{}
{}{}│   │|   |{}{}| ● || ◼ || ◼ || ◼ || ◀ |{}{}|   ||   ||   ||   |{}{}| ● || ◼ || ◼ || ◀ |{}{}|   |{}
{}{}└───┘└───┘{}{}└───┘└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘└───┘└───┘└───┘{}{}└───┘{}
"""

# Color formatting, one entry for each {} placeholder in BOARD_TEXT
BOARD_COLORS = [
   BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, BG_RED, FG_WHITE, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_YELLOW, FG_WHITE, BG_CYAN, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, RESET_COLORS,
   BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, BG_YELLOW, FG_WHITE, BG_WHITE, FG_BLACK, RESET_COLORS,
]

# Generate the empty board
def _generateEmptyBoard():
   return BOARD_TEXT.format(*BOARD_COLORS)

# Apply the game state onto the empty board
def _applyGameState(board, game):
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
def renderBoard(game):
   return _applyGameState(_generateEmptyBoard(), game)

# Render the state of an empty game to stdout, for reference
if __name__ == "__main__":
   game = Game(players=4)
   board = renderBoard(game)
   print(board, end = "")
