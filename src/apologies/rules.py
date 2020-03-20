# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implements all rules related to game play.
"""

from enum import Enum
from typing import Sequence, Optional

import attr

from .game import Game, GameMode, PlayerColor, Card, Pawn

# For an adult-mode game, we deal out 5 cards
_ADULT_HAND = 5

# The start squares for each color
_START_SQUARE = {
    PlayerColor.RED: 4,
    PlayerColor.BLUE: 19,
    PlayerColor.YELLOW: 34,
    PlayerColor.GREEN: 49,
}


class ActionType(Enum):
    """Enumeration of all actions that a character can take."""

    MOVE_FROM_START = "Move from start"  # Move a pawn from start
    MOVE_FORWARD = "Move forward"  # Move a pawn forward a certain number of spaces
    MOVE_BACKARD = "Move backward"  # Move a pawn backward a certain number of spaces
    CHANGE_PLACES = "Change places"  # Change places, swapping two pawns on the board
    BUMP_TO_START = "Bump to start"  # Move a pawn from start, bumping another pawn off the board


@attr.s
class Action:
    """An action that can be taken as part of a move."""

    actiontype = attr.ib(type=ActionType)
    mine = attr.ib(type=Pawn)
    theirs = attr.ib(default=None, type=Optional[Pawn])
    squares = attr.ib(default=None, type=Optional[int])


@attr.s
class Move:

    """
    A player's move on the board, which consists of one or more actions

    Attributes:
        card(Card): the card that is being played by this move
        actions(:obj: List of :obj: Action): List of actions to execute
    """

    card = attr.ib(type=Card)
    actions = attr.ib(type=Sequence[Action])


@attr.s
class Rules:

    """
    Implements all rules related to game play.

    Attributes:
        mode(GameMode): The game mode
    """

    mode = attr.ib(type=GameMode)

    def start_game(self, game: Game) -> Game:
        """Start the game, returning a copy of game state."""
        if self.mode == GameMode.ADULT:
            Rules._setup_adult_mode(game)
        return game.copy()

    @staticmethod
    def _setup_adult_mode(game: Game) -> None:
        """Setup adult mode at the start of the game, which moves some pieces and deals some cards."""
        for player in game.players.values():
            player.pawns[0].move_to_square(_START_SQUARE[player.color])
        for _ in range(_ADULT_HAND):
            for player in game.players.values():
                player.hand.append(game.deck.draw())
