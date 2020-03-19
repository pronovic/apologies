# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Game engine that coordinates character actions to play a game.
"""

from typing import List, Dict
import attr
from .game import Game, GameMode, Player, PlayerColor, CardType
from .character import Character
from .util import CircularQueue

# For an adult-mode game, we deal out 5 cards
ADULT_HAND = 5

# The start squares for each color
_START_SQUARE = {
    PlayerColor.RED: 4,
    PlayerColor.BLUE: 19,
    PlayerColor.YELLOW: 34,
    PlayerColor.GREEN: 49,
}

# Whether a card draws again
_DRAW_AGAIN = {
    CardType.CARD_1: False,
    CardType.CARD_2: True,
    CardType.CARD_3: False,
    CardType.CARD_4: False,
    CardType.CARD_5: False,
    CardType.CARD_7: False,
    CardType.CARD_8: False,
    CardType.CARD_10: False,
    CardType.CARD_11: False,
    CardType.CARD_12: False,
    CardType.CARD_APOLOGIES: False,
}


@attr.s
class _Player:
    """Internal data for a character."""

    player = attr.ib(type=Player)
    character = attr.ib(type=Character)
    winner = attr.ib(init=False, default=False)
    score = attr.ib(init=False, default=0)


@attr.s
class Engine:

    """
    Game engine that coordinates character actions in a game.

    Attributes:
        mode(GameMode): The game mode
        characters(:obj: list of :obj: Character): Characters playing the game
        started(boolean): Whether the game is started
        completed(boolean): Whether the game is completed
        game(Game): The current state of the game, not to be modified by callers
        _players(:obj: list of :obj: _Player): Internal list of players
        _queue(CircularQueue): Queue that controls the order in which characters play
    """

    mode = attr.ib(init=False, default=GameMode.STANDARD, type=GameMode)
    characters = attr.ib(type=List[Character])
    started = attr.ib(init=False, default=False, type=bool)
    completed = attr.ib(init=False, default=False, type=bool)
    game = attr.ib(init=False, type=Game)
    _players = attr.ib(init=False, type=Dict[PlayerColor, _Player])
    _queue = attr.ib(init=False, type=CircularQueue)
