# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implementations for command-line (CLI) tools.
"""

import sys
from typing import List, IO, Any

from apologies.game import Game
from apologies.render import render_board


def _render(unused_argv: List[str], stdout: IO[str], unused_stderr: IO[str]) -> None:
    """
    Execute the render script.
    """
    game = Game(4)
    board = render_board(game)
    stdout.write("%s" % board)


def _example(argv: List[str], stdout: IO[str], stderr: IO[str]) -> None:  # pylint: disable: unused-argument
    """
    Execute the example script, which just writes some input to its outputs.
    """
    stdout.write("Hello, stdout: %s\n" % argv[0])
    stderr.write("Hello, stderr: %s\n" % argv[0])


def _lookup_method(method: str) -> Any:
    """
    Look up the method in this module with the passed-in name.
    """
    module = sys.modules[__name__]
    return getattr(module, "_%s" % method)


def cli(script: str) -> None:
    """
    Run the main routine for the named script.

    Args:
        script(str): Name of the script to execute
    """
    _lookup_method(script)(sys.argv, sys.stdout, sys.stderr)
