# vim: set ft=python ts=4 sw=4 expandtab:
# ruff: noqa: T201, ANN001

"""
Implements a quick'n'dirty game-playing demo using curses.
"""

import curses
import sys
from curses import endwin
from signal import SIGWINCH, signal
from time import sleep

from apologies.engine import Character, Engine
from apologies.game import GameMode
from apologies.render import render_board
from apologies.source import CharacterInputSource

# Minimum terminal size needed to support the demo
_MIN_COLS = 155
_MIN_ROWS = 58


class TerminalSizeError(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg


def _render_hand(player) -> str:
    """Return a string describing the cards in a player's hand."""
    if not player.hand:
        return "n/a"
    return "%s" % [card.cardtype.value for card in sorted(player.hand)]


def _draw(stdscr, board, state, history) -> None:
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


# pylint: disable=too-many-positional-arguments
def _refresh(source, engine, game, delay_sec, stdscr, board, state, history) -> None:  # noqa: PLR0917,PLR0913
    """Refresh the dynamic portions of the screen."""
    _refresh_screen(source, engine, delay_sec, game, stdscr)
    _refresh_board(game, board)
    _refresh_state(source, engine, delay_sec, game, state)
    _refresh_history(game, history)


def _refresh_screen(_source, _engine, _game, _delay_sec, stdscr) -> None:
    stdscr.border()
    stdscr.addstr(1, 95, "APOLOGIES DEMO")
    stdscr.addstr(1, 138, "CTRL-C TO EXIT")
    stdscr.move(_MIN_ROWS - 2, _MIN_COLS - 2)  # bottom-right corner
    stdscr.refresh()


def _refresh_board(game, board) -> None:
    """Refresh the game board display section of the screen."""
    board.clear()
    board.border()

    for row, line in enumerate(render_board(game).splitlines(), start=0):
        board.addstr(row, 1, line)

    board.refresh()


def _refresh_state(source, engine, delay_sec, game, state) -> None:
    """Refresh the game state section of the screen."""
    state.clear()
    state.border()

    state.addstr(1, 2, "CONFIGURATION")
    state.addstr(3, 3, f"Players..: {engine.players}")
    state.addstr(4, 3, f"Mode.....: {engine.mode.value}")
    state.addstr(5, 3, f"Source...: {type(source).__name__}")
    state.addstr(6, 3, f"Delay....: {delay_sec} seconds")
    state.addstr(7, 3, f"State....: {engine.state}")

    row = 10
    for player in game.players.values():
        state.addstr(row + 0, 2, f"{player.color.name} PLAYER")
        state.addstr(row + 2, 3, f"Hand.....: {_render_hand(player)}")
        state.addstr(row + 3, 3, "Pawns....:")
        state.addstr(row + 4, 6, f"{player.pawns[0]}")
        state.addstr(row + 5, 6, f"{player.pawns[1]}")
        state.addstr(row + 6, 6, f"{player.pawns[2]}")
        state.addstr(row + 7, 6, f"{player.pawns[3]}")
        row += 10

    state.refresh()


def _refresh_history(game, history) -> None:
    """Refresh the game history section of the screen."""
    history.clear()
    history.border()

    row = 1
    for entry in game.history[-1:]:
        history.addstr(row, 2, f"{entry}")
        row += 1

    history.refresh()


def _main(
    stdscr,
    *,
    source: CharacterInputSource,
    engine: Engine,
    delay_sec: float,
    exit_immediately: bool,
) -> None:
    """Main routine for the Python curses application, intended to be wrapped by curses.wrapper()"""

    rows, columns = stdscr.getmaxyx()
    if columns < _MIN_COLS or rows < _MIN_ROWS:
        raise TerminalSizeError(f"Minimum terminal size is {_MIN_COLS}x{_MIN_ROWS}, but yours is {columns}x{rows}")

    board = curses.newwin(53, 90, 1, 3)
    state = curses.newwin(52, 59, 2, 94)
    history = curses.newwin(3, 150, 54, 3)

    # See https://stackoverflow.com/a/57205676/2907667
    def resize(_signum=None, _frame=None) -> None:
        endwin()
        _draw(stdscr, board, state, history)

    signal(SIGWINCH, resize)
    resize()

    complete = False
    while not complete:  # loop until the user CTRL-C's the application
        if engine.completed:
            if exit_immediately:
                complete = True
                break
        else:
            game = engine.play_next()
            _refresh(source, engine, game, delay_sec, stdscr, board, state, history)
        sleep(delay_sec)


def _force_minimum_size() -> None:
    """Force an xterm to resize via a control sequence."""

    # As of 2020, this worked in both the standard Apple terminal and Debian xterm.
    #
    # In 2022, it no longer works in Debian.  Even in the Apple terminal, it only
    # works if the terminal font and monitor actually allow the requested size, and
    # there's no indication whether it worked or not.
    #
    # I'm apparently using a slightly larger font now than when I originally wrote
    # this code, and these days my terminal can't successfully resize past 155x59 on
    # my Macbook.  The original rendering needed at least 155x70.  To deal with this,
    # I added the TerminalSizeError error handling block (above) to explictly detect
    # that it isn't possible to render the board, and I also adjusted the rendering
    # to work in a slightly smaller terminal.
    #
    # See: https://apple.stackexchange.com/a/47841/249172

    print(f"\u001b[8;{_MIN_ROWS};{_MIN_COLS}t")
    sleep(0.5)  # wait for the window to finish resizing; if we try to render before it's done, the window gets hosed up


def run_demo(
    *,
    players: int,
    mode: GameMode,
    source: CharacterInputSource,
    delay_sec: float,
    exit_immediately: bool,
) -> None:
    """
    Run the quick'n'dirty demo in a terminal window.

    Args:
        players(int): Number of players in the game
        mode(GameMode): The game mode
        source(CharacterInputSource): The source to use for choosing player moves
        delay_sec(float): The delay between turns when executing the game
        exit_immediately(bool): If True, exit immediately when the game is complete
    """
    try:
        characters = [Character(name=f"Player {player}", source=source) for player in range(players)]
        engine = Engine(mode=mode, characters=characters)
        engine.start_game()
        _force_minimum_size()
        curses.wrapper(
            _main,
            source=source,
            engine=engine,
            delay_sec=delay_sec,
            exit_immediately=exit_immediately,
        )
    except KeyboardInterrupt:  # users get out using CTRL-C
        print("Demo completed")
        sys.exit(0)
    except TerminalSizeError as e:
        print(e.msg)
        sys.exit(1)
