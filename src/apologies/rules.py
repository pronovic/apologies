# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implements rules related to game play.
"""

from enum import Enum
from typing import Optional, Sequence

import attr

from .game import ADULT_HAND, Card, CardType, Game, GameMode, Pawn, PlayerColor

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


class ValidationError(ValueError):
    """Indicates that a move is invalid."""


# noinspection PyProtectedMember
@attr.s
class Rules:

    """
    Implements rules related to game play.

    Attributes:
        mode(GameMode): The game mode
    """

    mode = attr.ib(type=GameMode)

    # noinspection PyMethodMayBeStatic
    def draw_again(self, card: Card) -> bool:
        """Whether the player gets to draw again based on the passed-in card."""
        return _DRAW_AGAIN[card.cardtype]

    def start_game(self, game: Game) -> None:
        """
        Start the game.

        Args:
            game(Game): Game to operate on
        """
        if game.started:
            raise ValueError("Game is already started")
        game.track("Game started with mode: %s" % self.mode)
        if self.mode == GameMode.ADULT:
            Rules._setup_adult_mode(game)

    def execute_move(self, game: Game, color: PlayerColor, move: Move) -> None:
        """
        Execute a player's move, updating game state.

        Args:
            game(Game): Game to operate on
            color(PlayerColor): Color of the player associated with the move
            move(Move): Move to validate

        Raises:
            ValidationError: If the move is not valid
        """
        # TODO: implement Rules.execute_move()

    @staticmethod
    def _setup_adult_mode(game: Game) -> None:
        """Setup adult mode at the start of the game, which moves some pieces and deals some cards."""
        for player in game.players.values():
            player.pawns[0].position.move_to_square(_START_SQUARE[player.color])
        for _ in range(ADULT_HAND):
            for player in game.players.values():
                player.hand.append(game.deck.draw())
