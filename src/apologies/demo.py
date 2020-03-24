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
from .source import CharacterInputSource

# Minimum terminal size needed to support the demo
MIN_COLS = 155
MIN_ROWS = 65


def _render_history(entry):
    """Return a history entry."""
    timestamp = entry.timestamp.to_time_string()
    color = "General" if not entry.color else "%s PLAYER" % entry.color.name
    action = entry.action
    return "[%s] %s - %s" % (timestamp, color, action)


# pylint: disable=no-else-return
def _render_hand(player):
    """Return a string describing the cards in a player's hand."""
    if not player.hand:
        return "n/a"
    else:
        return "%s" % [card.cardtype.value for card in sorted(player.hand)]


# pylint: disable=no-else-return
def _render_position(position):
    """Return a string describing a position."""
    if position.home:
        return "home"
    elif position.start:
        return "start"
    elif position.safe is not None:
        return "safe %d" % position.safe
    else:
        return "square %d" % position.square


def _render_pawn(pawn):
    """Return a string describing a player's pawns."""
    return "%s -> %s" % (pawn.name, _render_position(pawn.position))


def _draw(stdscr, board, state, history):
    """Draw the static portions of the screen."""
    stdscr.clear()
    stdscr.border()
    stdscr.addstr(1, 4, "APOLOGIES DEMO")
    stdscr.addstr(1, 138, "CTRL-C TO EXIT")
    stdscr.refresh()

    board.border()
    board.refresh()

    state.border()
    state.refresh()

    history.border()
    history.refresh()


def _refresh(source, engine, game, stdscr, board, state, history):
    """Refresh the dynamic portions of the screen."""
    _refresh_board(source, engine, game, board)
    _refresh_state(source, engine, game, state)
    _refresh_history(source, engine, game, history)
    stdscr.move(MIN_ROWS - 2, MIN_COLS - 2)  # bottom-right corner
    stdscr.refresh()


def _refresh_board(unused_source, unused_engine, unused_game, board):
    """Refresh the game board display."""
    # TODO: figure out how to render the board
    # index = 0
    # for line in render_board(game).splitlines():
    #     board.addstr(index, 0, line.encode("utf-8"))
    board.refresh()


def _refresh_state(source, engine, game, state):
    """Refresh the game state."""

    state.addstr(1, 2, "CONFIGURATION")
    state.addstr(3, 3, "Players..: %d" % engine.players)
    state.addstr(4, 3, "Mode.....: %s" % engine.mode.value)
    state.addstr(5, 3, "Source...: %s" % type(source).__name__)
    state.addstr(6, 3, "State....: %s" % engine.state)

    start = 9
    for player in game.players.values():
        state.addstr(start + 0, 2, "%s PLAYER" % player.color.name)
        state.addstr(start + 2, 3, "Hand.....: %s" % _render_hand(player))
        state.addstr(start + 3, 3, "Pawns....:")
        state.addstr(start + 4, 6, "%s" % _render_pawn(player.pawns[0]))
        state.addstr(start + 5, 6, "%s" % _render_pawn(player.pawns[1]))
        state.addstr(start + 6, 6, "%s" % _render_pawn(player.pawns[2]))
        state.addstr(start + 7, 6, "%s" % _render_pawn(player.pawns[3]))
        start += 10

    state.refresh()


def _refresh_history(unused_source, unused_engine, game, history):
    """Refresh the game history."""
    start = 1
    for entry in game.history[-5:]:
        history.addstr(start, 3, "%s" % _render_history(entry))
    history.refresh()


def _main(stdscr, source: CharacterInputSource, engine: Engine):
    """Main routine for the Python curses application, intended to be wrapped by curses.wrapper()"""

    board = curses.newwin(50, 90, 3, 3)
    state = curses.newwin(50, 59, 3, 94)
    history = curses.newwin(11, 150, 53, 3)

    def resize(unused_signum=None, unused_frame=None):
        endwin()  # this could lead to crashes, per https://stackoverflow.com/a/57205676/2907667
        _draw(stdscr, board, state, history)

    signal(SIGWINCH, resize)
    resize()

    while True:
        game = engine.play_next()
        _refresh(source, engine, game, stdscr, board, state, history)
        sleep(5)


def _force_resize(cols: int, rows: int) -> None:
    """
    Force an xterm to resize via a control sequence.
    I've tested that this works in the standard Apple terminal and a Debian xterm.
    See: https://apple.stackexchange.com/a/47841/249172
    """
    print("\u001b[8;%d;%dt" % (rows, cols))


def run_demo(players: int, mode: GameMode, source: CharacterInputSource) -> None:
    characters = [Character(name="Player %d" % player, source=source) for player in range(players)]
    engine = Engine(mode=mode, characters=characters)
    engine.start_game()
    _force_resize(MIN_COLS, MIN_ROWS)
    curses.wrapper(_main, source, engine)
