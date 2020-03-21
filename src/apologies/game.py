# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Classes that track game state.

Note that these classes track game state, but do not implement game rules.  The
only validations are to prevent changes that literally cannot be represented in
game state, such as selecting an invalid square.  All other rules (such as the
restriction that only one pawn can occupy a space, or the act of sliding down a
slider, etc.) are implemented in the rules module, using the methods available on these
classes.

In many cases, private attributes are accessible in the constructor to support
serialization and deserialization.  In general, callers should not pass in optional
constructor arguments and should not modify public attributes if an alternate method
is available for use.

Attributes:
    MIN_PLAYERS(int): Minimum number of players in a game
    MAX_PLAYERS(int): Maximum number of players in a game
    PAWNS(int): Number of pawns per player
    SAFE_SQUARES(int): Number of safe squares for each color
    BOARD_SQUARES(int): Number of squares around the outside of the board
    ADULT_HAND(int): Number of cards in a player's hand for an adult mode game
    DECK_COUNTS(dict): Dictionary from card name to number of cards in a standard deck
    DECK_SIZE(int): The total expected size of a complete deck
"""

from __future__ import annotations  # see: https://stackoverflow.com/a/33533514/2907667

import random
from enum import Enum
from typing import Dict, List, Optional

import attr
import orjson
import pendulum
from pendulum.datetime import DateTime

from .util import CattrConverter

# A game consists of 2-4 players
MIN_PLAYERS = 2
MAX_PLAYERS = 4

# There are 4 pawns per player, numbered 0-3
PAWNS = 4

# There are 5 safe squares for each color, numbered 0-4
SAFE_SQUARES = 5

# There are 60 squares around the outside of the board, numbered 0-59
BOARD_SQUARES = 60


class GameMode(Enum):
    """Available game play modes."""

    STANDARD = "Standard"
    ADULT = "Adult"


class PlayerColor(Enum):
    """Enumeration of all player colors, listed in order of use."""

    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"


class CardType(Enum):
    """All legal types of cards."""

    CARD_1 = "1"
    CARD_2 = "2"
    CARD_3 = "3"
    CARD_4 = "4"
    CARD_5 = "5"
    CARD_7 = "7"
    CARD_8 = "8"
    CARD_10 = "10"
    CARD_11 = "11"
    CARD_12 = "12"
    CARD_APOLOGIES = "Apologies"


# For an adult-mode game, we deal out 5 cards
ADULT_HAND = 5

# Deck definitions
DECK_COUNTS = {
    CardType.CARD_1: 5,
    CardType.CARD_2: 4,
    CardType.CARD_3: 4,
    CardType.CARD_4: 4,
    CardType.CARD_5: 4,
    CardType.CARD_7: 4,
    CardType.CARD_8: 4,
    CardType.CARD_10: 4,
    CardType.CARD_11: 4,
    CardType.CARD_12: 4,
    CardType.CARD_APOLOGIES: 4,
}
DECK_SIZE = sum(DECK_COUNTS.values())


@attr.s(frozen=True)
class Card:
    """
    A card in a deck or in a player's hand.

    Attributes:
        id(str): Unique identifier for this card
        cardtype(CardType): The type of the card
    """

    id = attr.ib(type=str)
    cardtype = attr.ib(type=CardType)


@attr.s
class Deck:
    """
    The deck of cards associated with a game.

    Callers should not pass in constructor arguments. These are accessible to
    support serialization and deserialization.
    """

    _draw_pile = attr.ib(type=Dict[str, Card])
    _discard_pile = attr.ib(type=Dict[str, Card])

    @_draw_pile.default
    def _init_draw_pile(self) -> Dict[str, Card]:
        pile = {}
        cardid = 0
        for card in CardType:
            for _ in range(DECK_COUNTS[card]):
                pile["%d" % cardid] = Card("%d" % cardid, card)
                cardid += 1
        return pile

    @_discard_pile.default
    def _init_discard_pile(self) -> Dict[str, Card]:
        return {}

    def draw(self) -> Card:
        """Draw a random card from the draw pile."""
        if len(self._draw_pile) < 1:
            # this is equivalent to shuffling the discard pile into the draw pile
            for card in list(self._discard_pile.values()):
                self._discard_pile.pop(card.id)
                self._draw_pile[card.id] = card
        if len(self._draw_pile) < 1:
            raise ValueError("No cards available in deck")
        return self._draw_pile.pop(random.choice(list(self._draw_pile.keys())))

    def discard(self, card: Card) -> None:
        """Discard back to the discard pile."""
        if card.id in self._draw_pile or card.id in self._discard_pile:
            raise ValueError("Card already exists in deck")
        self._discard_pile[card.id] = card


@attr.s
class Pawn:
    """
    A pawn on the board, belonging to a player.

    Callers should not pass in or directly modify the start, home, safe, or square
    attributes.  These are accessible to support serialization and deserialization.
    Instead, use the provided methods to safely modify the object in-place.

    Attributes:
        color(str): The color of this pawn
        index(int): Zero-based index of this pawn for a given user
        name(str): The full name of this pawn as "color-index"
        start(boolean): Whether this pawn resides in its start area
        home(boolean): Whether this pawn resides in its home area
        safe(int): Zero-based index of the square in the safe area where this pawn resides
        square(int): Zero-based index of the square on the board where this pawn resides
    """

    color = attr.ib(type=PlayerColor)
    index = attr.ib(type=int)
    name = attr.ib(type=str)
    start = attr.ib(default=True, type=bool)
    home = attr.ib(default=False, type=bool)
    safe = attr.ib(default=None, type=Optional[int])
    square = attr.ib(default=None, type=Optional[int])

    @name.default
    def _default_name(self) -> str:
        return "%s-%s" % (self.color.value, self.index)

    def move_to_start(self) -> None:
        """Move the pawn back to its start area."""
        self.start = True
        self.home = False
        self.safe = None
        self.square = None

    def move_to_home(self) -> None:
        """Move the pawn to its home area."""
        self.start = False
        self.home = True
        self.safe = None
        self.square = None

    def move_to_safe(self, square: int) -> None:
        """
        Move the pawn to a square in its safe area.

        Args:
            square(int): Zero-based index of the square in the safe area

        Raises:
            ValueError: If the square is not valid
        """

        if square not in range(SAFE_SQUARES):
            raise ValueError("Invalid square")
        self.start = False
        self.home = False
        self.safe = square
        self.square = None

    def move_to_square(self, square: int) -> None:
        """
        Move the pawn to a square on the board.

        Args:
            square(int): Zero-based index of the square on the board where this pawn resides

        Raises:
            ValueError: If the square is not valid
        """

        if square not in range(BOARD_SQUARES):
            raise ValueError("Invalid square")
        self.start = False
        self.home = False
        self.safe = None
        self.square = square


@attr.s
class Player:
    """
    A player, which has a color and a set of pawns.

    Callers should not pass in the hand and pawns constructor arguments.  These
    are accessible to support serialization and deserialization.

    Attributes:
        color(str): The color of the player
        hand(:obj:`list` of :obj:`Card`): List of cards in the player's hand
        pawns(:obj:`list` of :obj:`Pawn`): List of all pawns belonging to the player
    """

    color = attr.ib(type=PlayerColor)
    hand = attr.ib(type=List[Card])
    pawns = attr.ib(type=List[Pawn])

    @hand.default
    def _init_hand(self) -> List[Card]:
        return []

    @pawns.default
    def _init_pawns(self) -> List[Pawn]:
        return [Pawn(self.color, index) for index in range(0, PAWNS)]

    def find_first_pawn_in_start(self) -> Optional[Pawn]:
        """Find the first pawn in the start area, if any."""
        for pawn in self.pawns:
            if pawn.start:
                return pawn
        return None

    def all_pawns_in_home(self) -> bool:
        """Whether all of this user's pawns are in home."""
        for pawn in self.pawns:
            if not pawn.home:
                return False
        return True


@attr.s
class History:
    """Tracks a move made by a player."""

    action = attr.ib(type=str)
    color = attr.ib(default=None, type=Optional[PlayerColor])
    timestamp = attr.ib(type=DateTime)

    @timestamp.default
    def _init_timestamp(self) -> DateTime:
        return pendulum.now(pendulum.UTC)


@attr.s
class Game:
    """
    The game, consisting of state for a set of players.

    Callers should not pass in optional constructor arguments.  These are accessible
    to support serialization and deserialization.

    Attributes:
        playercount(int): Number of players in the game
        players(:obj:`dict` of :obj:`Player`): All players in the game
        deck(Deck): The deck of cards for the game
    """

    converter = CattrConverter()

    playercount = attr.ib(type=int)
    players = attr.ib(type=Dict[PlayerColor, Player])
    deck = attr.ib(type=Deck)
    history = attr.ib(type=List[History])

    @playercount.validator
    def _check_playercount(self, attribute: str, value: int) -> None:
        if value < MIN_PLAYERS or value > MAX_PLAYERS:
            raise ValueError("Invalid number of players")

    @players.default
    def _init_players(self) -> Dict[PlayerColor, Player]:
        return {color: Player(color) for color in list(PlayerColor)[: self.playercount]}

    @deck.default
    def _init_deck(self) -> Deck:
        return Deck()

    @history.default
    def _init_history(self) -> List[History]:
        return []

    @property
    def started(self) -> bool:
        """Whether the game has been started."""
        return len(self.history) > 0  # if there is any history the game has been started

    @property
    def completed(self) -> bool:
        """Whether the game is completed."""
        for player in self.players.values():
            if player.all_pawns_in_home():
                return True
        return False

    def copy(self) -> Game:
        """Return a fully-independent copy of the game."""
        return Game.converter.structure(Game.converter.unstructure(self), Game)  # type: ignore

    def to_json(self) -> str:
        """Serialize the game state to JSON."""
        return orjson.dumps(Game.converter.unstructure(self), option=orjson.OPT_INDENT_2).decode("utf-8")  # type: ignore

    @staticmethod
    def from_json(data: str) -> Game:
        """Deserialize the game state from JSON."""
        return Game.converter.structure(orjson.loads(data), Game)  # type: ignore

    def track(self, action: str, player: Optional[Player] = None) -> None:
        """Tracks a move made by a player."""
        self.history.append(History(action, player.color if player else None))

    def find_pawn_on_square(self, square: int) -> Optional[Pawn]:
        """Return the pawn on the indicated square, or None."""
        for player in self.players.values():
            for pawn in player.pawns:
                if pawn.square == square:
                    return pawn
        return None
