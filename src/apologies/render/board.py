# -*- coding: utf-8 -*-
# vim: set ft=python ts=3 sw=3 expandtab: 

# This is kind of ugly.  It was built by hand and all of the mappings, etc. are hardcoded.
# Since it's intended as a development and debugging tool, I don't really care too much
# about how nice it looks.

from apologies.render.colors import *

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

# ★ for a player, maybe flashing?

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
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
   BG_GREEN, FG_WHITE, BG_CYAN, BG_RED, FG_WHITE, BG_CYAN, BG_BLUE, FG_WHITE, RESET_COLORS,
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

def renderBoard():
   print(BOARD_TEXT.format(*BOARD_COLORS))
