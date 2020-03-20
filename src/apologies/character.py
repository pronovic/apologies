# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Player character interfaces.
"""

from abc import ABC, abstractmethod
from typing import Optional

import attr

from .game import Game, GameMode, Player, Card
from .rules import Move


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
