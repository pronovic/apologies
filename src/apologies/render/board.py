# -*- coding: utf-8 -*-
# vim: set ft=python ts=3 sw=3 expandtab: 

# This is kind of ugly.  It was built by hand and all of the mappings, etc. are hardcoded.
# Since it's intended as a development and debugging tool, I don't really care too much
# about how nice it looks.

from apologies.render.colors import *

# The string that identifies a piece for each color player
RED_PIECE = "R"
BLUE_PIECE = "B"
GREEN_PIECE = "G"
YELLOW_PIECE = "Y"

# These indexes aren't easily predictible, because of the variable length of formatting characters

# Index into BOARD_TEXT where a piece can be placed into a specific square
# Squares are numbered from starting from the upper left, in a clockwise direction
# Only a single piece can occupy a square
SQUARE = [
160, 177, 182, 187, 192, 209, 214, 219, 224, 241, 246, 251, 256, 261, 278, 283, 724, 1185, 1646, 2090,
2517, 2910, 3303, 3696, 4089, 4482, 4926, 5370, 5831, 6309, 6730, 6713, 6708, 6703, 6698, 6681, 6676,
6671, 6666, 6649, 6644, 6639, 6634, 6629, 6612, 6607, 6166, 5705, 5244, 4800, 4373, 3980, 3587, 3194,
2801, 2408, 1964, 1520, 1059, 581, ]

# Indexes in BOARD_TEXT where a piece can be placed into a start location, for the red player
# There are 4 arbitrary spaces for the 4 available pieces
RED_START = [ 1111, 1113, 1115, 1117, ]

# Indexes in BOARD_TEXT where a piece can be placed into a safe location, for the red player
# Safe squares are numbered from 0-4 starting from the bottom
# Only a single piece can occupy a safe square
RED_SAFE = [ 608, 1086, 1547, 1991, 2435, ]

# Indexes in BOARD_TEXT where a piece can be placed into a home location, for the red player
# There are 4 arbitrary spaces for the 4 available pieces
RED_HOME = [ 3086, 3088, 3090, 3092, ]

# Indexes in BOARD_TEXT where a piece can be placed into a start location, for the blue player
# There are 4 arbitrary spaces for the 4 available pieces
BLUE_START = [ 2060, 2062, 2064, 2066, ]

# Indexes in BOARD_TEXT where a piece can be placed into a safe location, for the blue player
# Safe squares are numbered from 0-4 starting from the bottom
# Only a single piece can occupy a safe square
BLUE_SAFE = [ 1180, 1175, 1170, 1165, 1160, ]

# Indexes in BOARD_TEXT where a piece can be placed into a home location, for the blue player
# There are 4 arbitrary spaces for the 4 available pieces
BLUE_HOME = [ 1148, 1150, 1152, 1154, ]

# Indexes in BOARD_TEXT where a piece can be placed into a start location, for the green player
# There are 4 arbitrary spaces for the 4 available pieces
GREEN_START = [ 4972, 4974, 4976, 4978, ]

# Indexes in BOARD_TEXT where a piece can be placed into a safe location, for the green player
# Safe squares are numbered from 0-4 starting from the bottom
# Only a single piece can occupy a safe square
GREEN_SAFE = [ 5710, 5715, 5720, 5725, 5730, ]

# Indexes in BOARD_TEXT where a piece can be placed into a home location, for the green player
# There are 4 arbitrary spaces for the 4 available pieces
GREEN_HOME = [ 5885, 5887, 5889, 5891, ]

# Indexes in BOARD_TEXT where a piece can be placed into a start location, for the yellow player
# There are 4 arbitrary spaces for the 4 available pieces
YELLOW_START = [ 5921, 5923, 5925, 5927, ]

# Indexes in BOARD_TEXT where a piece can be placed into a safe location, for the yellow player
# Safe squares are numbered from 0-4 starting from the bottom
# Only a single piece can occupy a safe square
YELLOW_SAFE = [ 6282, 5804, 5343, 4899, 4455, ]

# Indexes in BOARD_TEXT where a piece can be placed into a home location, for the yellow player
# There are 4 arbitrary spaces for the 4 available pieces
YELLOW_HOME = [ 3928, 3930, 3932, 3934, ]

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

# Render the board to stdout
def renderBoard():
   print(BOARD_TEXT.format(*BOARD_COLORS))

