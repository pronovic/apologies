# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Characters and the actions they can take.
"""

from abc import ABC, abstractmethod
from typing import Sequence, Optional

import attr

from .game import Game, Player, Card, Pawn


@attr.s
class Action:
    """An action that can be taken as part of a move."""


@attr.s
class MoveFromStartAction(Action):
    """Move a pawn from start."""


@attr.s
class MoveForwardAction(Action):

    """Move a pawn forward a certain number of spaces."""

    pawn = attr.ib(type=Pawn)
    spaces = attr.ib(type=int)


@attr.s
class MoveBackwardAction(Action):

    """Move a pawn backward a certain number of spaces."""

    pawn = attr.ib(type=Pawn)
    spaces = attr.ib(type=int)


@attr.s
class ChangePlacesAction(Action):

    """Change places, swapping two pawns on the board."""

    mine = attr.ib(type=Pawn)
    theirs = attr.ib(type=Pawn)


@attr.s
class BumpToStartAction(Action):

    """Move pawn from start, bumping another pawn off the board."""

    bumped = attr.ib(type=Pawn)


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


class CharacterInputSource(ABC):

    """A generic source of input for a character, which could be a person or could be computer-driven."""

    @abstractmethod
    def construct_move(self, game: Game, player: Player, card: Optional[Card] = None) -> Move:
        """
        Construct the next move for a player.

        Note: the passed-in game, player, and card must not be modified.

        Args:
            game(Game): Current state of the game
            player(Player): Current state of the player within the game
            card(Card, optional): The card to play, or None if move should come from player's hand

        Returns:
            Move: the player's next move
        """


@attr.s
class Character:

    """
    A character that plays a game, which could be a person or could be computer-driven.

    Attributes:
        name(str): The name of this character
        game(Game): The state of the underlying game
        player(Player): The state of the underlying player
        source(CharacterInputSource): The user input source from which moves are taken
    """

    name = attr.ib(type=str)
    game = attr.ib(type=Game)
    player = attr.ib(type=Player)
    source = attr.ib(type=CharacterInputSource)

    def construct_move(self, card: Optional[Card] = None) -> Move:
        """Construct the next move for a character via the user input source."""
        return self.source.construct_move(self.game, self.player, card)
