# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implements a game-playing demo using curses.
"""

import curses
from curses import endwin
from signal import SIGWINCH, signal
from time import sleep

from .engine import Character, Engine
from .game import GameMode
from .render import render_board
from .source import CharacterInputSource

# Minimum terminal size needed to support the demo
MIN_COLS = 155
MIN_ROWS = 70


def _render_history(entry):
    """Return a history entry."""
    timestamp = entry.timestamp.to_time_string()
    color = "General" if not entry.color else "%s" % entry.color.value
    action = entry.action
    return "[%s] %s - %s" % (timestamp, color, action)


# pylint: disable=no-else-return
def _render_hand(player):
    """Return a string describing the cards in a player's hand."""
    if not player.hand:
        return "n/a"
    else:
        return "%s" % [card.cardtype.value for card in sorted(player.hand)]


def _draw(stdscr, board, state, history):
    """Draw the static portions of the screen."""
    stdscr.clear()
    stdscr.border()
    stdscr.refresh()

    board.border()
    board.refresh()

    state.border()
    state.refresh()

    history.border()
    history.refresh()


def _refresh(source, engine, game, delay_sec, stdscr, board, state, history):
    """Refresh the dynamic portions of the screen."""
    _refresh_screen(source, engine, delay_sec, game, stdscr)
    _refresh_board(source, engine, delay_sec, game, board)
    _refresh_state(source, engine, delay_sec, game, state)
    _refresh_history(source, engine, delay_sec, game, history)


def _refresh_screen(unused_source, unused_engine, unused_game, unused_delay_sec, stdscr):
    stdscr.border()
    stdscr.addstr(1, 4, "APOLOGIES DEMO")
    stdscr.addstr(1, 138, "CTRL-C TO EXIT")
    stdscr.move(MIN_ROWS - 2, MIN_COLS - 2)  # bottom-right corner
    stdscr.refresh()


def _refresh_board(unused_source, unused_engine, unused_delay_sec, game, board):
    """Refresh the game board display."""
    board.clear()
    board.border()

    row = 0
    for line in render_board(game).splitlines():
        board.addstr(row, 1, line)
        row += 1

    board.refresh()


def _refresh_state(source, engine, delay_sec, game, state):
    """Refresh the game state."""
    state.clear()
    state.border()

    state.addstr(2, 2, "CONFIGURATION")
    state.addstr(4, 3, "Players..: %d" % engine.players)
    state.addstr(5, 3, "Mode.....: %s" % engine.mode.value)
    state.addstr(6, 3, "Source...: %s" % type(source).__name__)
    state.addstr(7, 3, "Delay....: %s seconds" % delay_sec)
    state.addstr(8, 3, "State....: %s" % engine.state)

    row = 11
    for player in game.players.values():
        state.addstr(row + 0, 2, "%s PLAYER" % player.color.name)
        state.addstr(row + 2, 3, "Hand.....: %s" % _render_hand(player))
        state.addstr(row + 3, 3, "Pawns....:")
        state.addstr(row + 4, 6, "%s" % player.pawns[0].log)
        state.addstr(row + 5, 6, "%s" % player.pawns[1].log)
        state.addstr(row + 6, 6, "%s" % player.pawns[2].log)
        state.addstr(row + 7, 6, "%s" % player.pawns[3].log)
        row += 10

    state.refresh()


def _refresh_history(unused_source, unused_engine, unused_delay_sec, game, history):
    """Refresh the game history."""
    history.clear()
    history.border()

    row = 1
    for entry in game.history[-9:]:
        history.addstr(row, 2, "%s" % _render_history(entry))
        row += 1

    history.refresh()


def _main(stdscr, source: CharacterInputSource, engine: Engine, delay_sec: float):
    """Main routine for the Python curses application, intended to be wrapped by curses.wrapper()"""

    board = curses.newwin(55, 90, 3, 3)
    state = curses.newwin(55, 59, 3, 94)
    history = curses.newwin(11, 150, 58, 3)

    def resize(unused_signum=None, unused_frame=None):
        endwin()  # this could lead to crashes, per https://stackoverflow.com/a/57205676/2907667
        _draw(stdscr, board, state, history)

    signal(SIGWINCH, resize)
    resize()

    while True:
        if not engine.completed:
            game = engine.play_next()
            _refresh(source, engine, game, delay_sec, stdscr, board, state, history)
        sleep(delay_sec)


def _force_resize(cols: int, rows: int) -> None:
    """
    Force an xterm to resize via a control sequence.
    I've tested that this works in the standard Apple terminal and a Debian xterm.
    See: https://apple.stackexchange.com/a/47841/249172
    """
    print("\u001b[8;%d;%dt" % (rows, cols))
    sleep(0.5)  # wait for the window to finish resizing, otherwise it doesn't always work right


def run_demo(players: int, mode: GameMode, source: CharacterInputSource, delay_sec: float) -> None:
    characters = [Character(name="Player %d" % player, source=source) for player in range(players)]
    engine = Engine(mode=mode, characters=characters)
    engine.start_game()
    _force_resize(MIN_COLS, MIN_ROWS)
    curses.wrapper(_main, source, engine, delay_sec)
