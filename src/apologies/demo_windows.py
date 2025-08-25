# vim: set ft=python ts=4 sw=4 expandtab:
# ruff: noqa: T201

"""
Stubs the demo, which does not run on Windows.
"""

from apologies.game import GameMode
from apologies.source import CharacterInputSource


def run_demo(
    *,
    _players: int,
    _mode: GameMode,
    _source: CharacterInputSource,
    _delay_sec: float,
    _exit_immediately: bool,
) -> None:
    """
    Stubs the demo, which does not run on Windows.
    """
    print("The demo is curses-based and does not run on Windows.")
