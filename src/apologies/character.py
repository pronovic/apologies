# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Characters and the actions they can take.
"""

from enum import Enum
from abc import ABC, abstractmethod
from typing import Sequence, Optional

import attr

from .game import Game, GameMode, Player, Card, Pawn


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


class CharacterInputSource(ABC):

    """A generic source of input for a character, which could be a person or could be computer-driven."""

    @abstractmethod
    def construct_move(
        self, game: Game, mode: GameMode, player: Player, card: Optional[Card] = None, invalid: Optional[bool] = False
    ) -> Move:
        """
        Construct the next move for a character.

        The passed-in game, player, and card must not be modified.

        If no move is possible, then return an empty list of actions.  If a card was passed-in, always
        attach it to the returned Move.  Otherwise, attach the card that is being played.  The attached
        card is always discarded back to the deck.

        Args:
            game(Game): Current state of the game
            mode(GameMode): Game mode
            player(Player): Current state of the player within the game
            card(Card, optional): The card to play, or None if move should come from player's hand
            invalid(bool, optional): Whether this call is because a previous move was invalid

        Returns:
            Move: the character's next move, an empty list if no move is possible and the turn is forfeit
        """


@attr.s
class Character:

    """
    A character that plays a game, which could be a person or could be computer-driven.

    Attributes:
        name(str): The name of this character
        source(CharacterInputSource): The character input source from which moves are taken
    """

    name = attr.ib(type=str)
    source = attr.ib(type=CharacterInputSource)

    def construct_move(
        self, game: Game, mode: GameMode, player: Player, card: Optional[Card] = None, invalid: Optional[bool] = False
    ) -> Move:
        """
        Construct the next move for a character via the user input source.

        Args:
            game(Game): Current state of the game
            mode(GameMode): Game mode
            player(Player): Current state of the player within the game
            card(Card, optional): The card to play, or None if move should come from player's hand
            invalid(bool, optional): Whether this call is because a previous move was invalid

        Returns:
            Move: the character's next move, an empty list if no move is possible and the turn is forfeit
        """
        return self.source.construct_move(game, mode, player, card, invalid)
