# vim: set ft=python ts=4 sw=4 expandtab:
# ruff: noqa: T201

"""
Implementations for command-line (CLI) tools.
"""

import argparse
import sys
from typing import IO, Any

from apologies.demo import run_demo
from apologies.game import MAX_PLAYERS, Game, GameMode
from apologies.render import render_board
from apologies.simulation import run_simulation
from apologies.source import source

# Constants used by the demo CLI
_DEMO_DEFAULT_PLAYERS = MAX_PLAYERS
_DEMO_DEFAULT_MODE = GameMode.STANDARD.name
_DEMO_MODE_CHOICES = [GameMode.STANDARD.name, GameMode.ADULT.name]
_DEMO_DEFAULT_SOURCE = "apologies.source.RandomInputSource"
_DEMO_DEFAULT_DELAY_SEC = 1

# Constants used by the simulation CLI
_SIM_DEFAULT_ITERATIONS = 10
_SIM_DEFAULT_OUT = "simulation.csv"


def demo(argv: list[str], _stdout: IO[str], _stderr: IO[str]) -> None:
    """Run a game with simulated players, displaying output on the terminal."""
    parser = argparse.ArgumentParser(
        description="Run a game with simulated players, displaying output on the terminal.",
        epilog=f"By default, the game runs in {_DEMO_DEFAULT_MODE} mode with "
        f"{_DEMO_DEFAULT_PLAYERS} players. A source is a class that "
        f"chooses a player's move.",
    )

    parser.add_argument(
        "--players",
        type=int,
        default=_DEMO_DEFAULT_PLAYERS,
        help="Number of simulated players in the game",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default=_DEMO_DEFAULT_MODE,
        choices=_DEMO_MODE_CHOICES,
        help="Choose the game mode",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=_DEMO_DEFAULT_SOURCE,
        help="Fully-qualified name of the character source",
    )
    parser.add_argument(
        "--exit",
        action="store_true",
        help="Exit immediately when the game completes",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=_DEMO_DEFAULT_DELAY_SEC,
        help="Delay between computer-generated moves (fractional seconds)",
    )

    args = parser.parse_args(args=argv[1:])
    run_demo(
        players=args.players,
        mode=GameMode[args.mode],
        source=source(args.source),
        delay_sec=args.delay,
        exit_immediately=args.exit,
    )


def simulation(argv: list[str], _stdout: IO[str], _stderr: IO[str]) -> None:
    """Run a simulation and display results."""
    parser = argparse.ArgumentParser(
        description="Run a simulation to see how well different character input sources behave.",
        epilog=f"Every combination of game mode, number of players, and input source is tested, "
        f"using {_SIM_DEFAULT_ITERATIONS} iterations by default.  A spreadsheet is "
        f"generated containing statistics on mean and median turns and duration to "
        f"win, as well as number of wins for each source.",
    )

    parser.add_argument(
        "--iter",
        type=int,
        default=_SIM_DEFAULT_ITERATIONS,
        help="Number of iterations per scenario",
    )

    parser.add_argument(
        "--out",
        type=str,
        default=_SIM_DEFAULT_OUT,
        help="Path to the output CSV file",
    )

    parser.add_argument(
        "source",
        type=str,
        nargs="+",
        help="Fully-qualified name of the character sources to test",
    )

    args = parser.parse_args(args=argv[1:])

    errors = []
    if args.iter <= 0:
        errors.append("simulation: error: there must be at least 1 iteration")

    if errors:
        parser.print_usage()
        print("\n".join(errors))
        sys.exit(1)

    run_simulation(iterations=args.iter, output=args.out, sources=[source(s) for s in args.source])


def render(_argv: list[str], stdout: IO[str], _stderr: IO[str]) -> None:
    """Render an empty board."""
    game = Game(4)
    board = render_board(game)
    stdout.write(f"{board}")


def example(argv: list[str], stdout: IO[str], stderr: IO[str]) -> None:
    """Execute the example script, which just writes some input to its outputs."""
    stdout.write(f"Hello, stdout: {argv[0]}\n")
    stderr.write(f"Hello, stderr: {argv[0]}\n")


def _lookup_method(method: str) -> Any:
    """Look up the method in this module with the passed-in name."""
    module = sys.modules[__name__]
    return getattr(module, f"{method}")


def cli(script: str) -> None:
    """
    Run the main routine for the named script.

    Args:
        script(str): Name of the script to execute
    """
    _lookup_method(script)(sys.argv, sys.stdout, sys.stderr)
