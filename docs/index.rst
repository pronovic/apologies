Apologies Python Library
========================

Release v\ |version|

.. image:: https://img.shields.io/pypi/l/apologies.svg
    :target: https://pypi.org/project/apologies/

.. image:: https://img.shields.io/pypi/wheel/apologies.svg
    :target: https://pypi.org/project/apologies/

.. image:: https://img.shields.io/pypi/pyversions/apologies.svg
    :target: https://pypi.org/project/apologies/

.. image:: https://github.com/pronovic/apologies/workflows/Test%20Suite/badge.svg
    :target: https://github.com/pronovic/apologies

.. image:: https://readthedocs.org/projects/apologies/badge/?version=latest&style=flat
    :target: https://apologies.readthedocs.io/en/latest/

Apologies_ is a Python library that implements a game similar to the Sorry_
board game.  It includes a console demo that plays the game with automated
players, intended for use by developers and not by end users.


Installation
------------

Install the package with pip::

    $ pip install apologies


Documentation
-------------

.. toctree::
   :maxdepth: 2
   :glob:


Playing a Game
---------------

In the Apologies system, a `Game` is played by one or more `Characters`.

A `Character` can either be human (a `Player Character`) or computer-driven
(a `Non-Player Character`).  The only difference between a `Player Character`
and a `Non-Player Character` is the `Character Input Source` tied to the
character.  A `Character Input Source` is a simply a class that decides how
to choose between available legal moves.  

The central class in the Apologies system is the Engine_, which coordinates
game play via a set of Characters_.  Game state is maintained in the Game_
class.  The Game_ class contains methods to serialize and deserialize game
state to and from JSON, which facilitates sharing state between two networked
components.

To play a game, you construct an Engine_, providing a GameMode_ and 2-4
Characters_ that will participate in the game.  The engine maintains
game state and coordinates the actions required to play the game.

The library comes with a single `Character Input Source` called RandomInputSource_,
which chooses randomly from among all legal moves.  More sophisticated 
sources can be created by implementing the CharacterInputSource_ interface.


Example Code
------------

This is a simple script to play a 2-player, standard-mode game and print
the results of each move::

    from time import sleep
    from apologies.engine import Engine, Character
    from apologies.game import GameMode
    from apologies.source import RandomInputSource

    p1 = Character("Player 1", source=RandomInputSource())
    p2 = Character("Player 2", source=RandomInputSource())
    engine = Engine(mode=GameMode.STANDARD, characters=[p1, p2])
    engine.start_game()
    while not engine.completed:
      state = engine.play_next()
      print("%s" % state.history[-1])
      sleep(1)

This example uses the RandomInputSource_, which chooses a legal move at random.
To create an interactive game for human players, you would implement your
own CharacterInputSource_ interface to get user input.


Running the Demo
----------------

While this is primarily a library, it includes a quick'n'dirty console demo
that plays a game with 2-4 automated players.  For instructions about how to
run the demo from codebase itself, see DEVELOPER.md_.  Otherwise, you can run
the demo from the installed package::

    $ python -c "from apologies.cli import cli; cli('demo')" --help
    usage: -c [-h] [--players PLAYERS] [--mode {STANDARD,ADULT}] [--source SOURCE]
              [--delay DELAY]

    Run a game with simulated players, displaying output on the terminal.

    optional arguments:
      -h, --help            show this help message and exit
      --players PLAYERS     Number of simulated players in the game
      --mode {STANDARD,ADULT}
                            Choose the game mode
      --source SOURCE       Fully-qualified name of the character source
      --delay DELAY         Delay between computer-generated moves (fractional
                            seconds)

    By default, the game runs in STANDARD mode with 4 players. A source is a class
    that chooses a player's move.

It's simplest to run a demo with the default arguments::

   $ python -c "from apologies.cli import cli; cli('demo')"

This runs a really fast game in adult mode with 3 players::

   $ python -c "from apologies.cli import cli; cli('demo')" -- --players=3 --mode=ADULT --delay=0.1

Exit the demo with `CTRL-C`.

`Note:` The demo only works inside a UNIX-style terminal window (like an
xterm or a MacOS terminal).  It doesn't work in a Windows console, because it
relies on the curses terminal library.  Some terminals (like iTerm2_) may
require extra configuration before the terminal can be resized properly
(see StackExchange_).

.. _Apologies: https://pypi.org/project/apologies
.. _Character: autoapi/apologies/engine/index.html#apologies.engine.Character
.. _CharacterInputSource: autoapi/apologies/source/index.html#apologies.source.CharacterInputSource
.. _Characters: autoapi/apologies/engine/index.html#apologies.engine.Character
.. _DEVELOPER.md: https://github.com/pronovic/apologies/blob/master/DEVELOPER.md#running-the-demo
.. _Engine: autoapi/apologies/engine/index.html#apologies.engine.Engine
.. _Game: autoapi/apologies/game/index.html#apologies.game.Game
.. _GameMode: autoapi/apologies/game/index.html#apologies.game.GameMode
.. _RandomInputSource: autoapi/apologies/source/index.html#apologies.source.RandomInputSource
.. _Sorry: https://en.wikipedia.org/wiki/Sorry!_(game)
.. _StackExchange: https://apple.stackexchange.com/a/47841/249172Z
.. _iTerm2: https://www.iterm2.com/
