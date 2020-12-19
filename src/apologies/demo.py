# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implements a quick'n'dirty game-playing demo using curses.
"""

import platform

from .game import GameMode
from .source import CharacterInputSource

if platform.system() == "Windows":
    from .demo_windows import run_demo as implementation  # pylint: disable=unused-import
else:
    from .demo_unix import run_demo as implementation  # pylint: disable=unused-import


def run_demo(players: int, mode: GameMode, source: CharacterInputSource, delay_sec: float) -> None:
    """
    Run the quick'n'dirty demo in a terminal window.

    Args:
        players(int): Number of players in the game
        mode(GameMode): The game mode
        source(CharacterInputSource): The source to use for choosing player moves
        delay_sec(float): The delay between turns when executing the game
    """
    implementation(players, mode, source, delay_sec)
