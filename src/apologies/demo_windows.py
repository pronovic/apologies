# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Stubs the demo, which does not run on Windows.
"""

from .game import GameMode
from .source import CharacterInputSource


# pylint: disable=unused-argument
def run_demo(players: int, mode: GameMode, source: CharacterInputSource, delay_sec: float) -> None:
    """
    Stubs the demo, which does not run on Windows.
    """
    print("The demo is curses-based and does not run on Windows.")
