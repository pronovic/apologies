# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Game engine that coordinates character actions to play a game.
"""

from typing import List
import attr
from .game import Game, GameMode, PlayerColor
from .character import Character
from .util import CircularQueue
from .rules import Rules


@attr.s
class Engine:

    """
    Game engine that coordinates character actions in a game.

    Attributes:
        mode(GameMode): The game mode
        characters(:obj: list of :obj: Character): Characters playing the game
        started(boolean): Whether the game is started
        completed(boolean): Whether the game is completed
        _game(Game): The current state of the game, not to be modified by callers
        _queue(CircularQueue): Queue that controls the order in which characters play
        _rules(Rules): Implements all rules related to game play
    """

    mode = attr.ib(type=GameMode)
    characters = attr.ib(type=List[Character])
    started = attr.ib(init=False, default=False, type=bool)
    completed = attr.ib(init=False, default=False, type=bool)
    _game = attr.ib(init=False, type=Game)
    _queue = attr.ib(init=False, type=CircularQueue[PlayerColor])
    _rules = attr.ib(init=False, type=Rules)

    @_game.default
    def _init_game(self) -> Game:
        return Game(playercount=len(self.characters))

    @_queue.default
    def _init_queue(self) -> CircularQueue[PlayerColor]:
        return CircularQueue(list(PlayerColor)[: len(self.characters)])

    @_rules.default
    def _init_rules(self) -> Rules:
        return Rules(self.mode)

    def start_game(self) -> Game:
        """Start the game, returning game state."""
        self.started = True
        self._game = self._rules.start_game(self._game)
        return self._game
