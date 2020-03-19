# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Classes that track game state.

Note that these classes track game state, but do not implement game rules.  The
only validations are to prevent changes that literally cannot be represented in
game state, such as selecting an invalid square.  All other rules (such as the
restriction that only one pawn can occupy a space, or the act of sliding down a
slider, etc.) are implemented in the play module, using the methods available on these
classes.

Attributes:
    ADULT_HAND: The size of a hand of cards for an adult-mode game
    MIN_PLAYERS(int): Minimum number of players in a game
    MAX_PLAYERS(int): Maximum number of players in a game
    PLAYER_RED(str): The red player color
    PLAYER_BLUE(str): The blue player color
    PLAYER_YELLOW(str): The yellow player color
    PLAYER_GREEN(str): The green player color
    PLAYER_COLORS(list): All available player colors, listed in order of use
    PAWNS(int): Number of pawns per player
    SAFE_SQUARES(int): Number of safe squares for each color
    BOARD_SQUARES(int): Number of squares around the outside of the board
    DECK_COUNTS: Dictionary from card name to number of cards in a standard deck
    DECK_SIZE: The total expected size of a complete deck
"""

import random
from enum import Enum
from typing import Optional, List, Dict

import attr

# A game consists of 2-4 players
MIN_PLAYERS = 2
MAX_PLAYERS = 4

# Each player gets one color
PLAYER_RED = "RED"
PLAYER_BLUE = "BLUE"
PLAYER_YELLOW = "YELLOW"
PLAYER_GREEN = "GREEN"
PLAYER_COLORS = [
    PLAYER_RED,
    PLAYER_YELLOW,
    PLAYER_GREEN,
    PLAYER_BLUE,
]  # order chosen so game works better for < 4 players

# There are 4 pawns per player, numbered 0-3
PAWNS = 4

# There are 5 safe squares for each color, numbered 0-4
SAFE_SQUARES = 5

# There are 60 squares around the outside of the board, numbered 0-59
BOARD_SQUARES = 60

# For an adult game, we deal out 5 cards
ADULT_HAND = 5


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
        id(int): Unique identifier for this card
        name(str): The name of the card
    """

    id = attr.ib(type=int)
    cardtype = attr.ib(type=CardType)


@attr.s
class Deck:
    """The deck of cards associated with a game."""

    _draw_pile = attr.ib(init=False, type=Dict[int, Card])
    _discard_pile = attr.ib(init=False, type=Dict[int, Card])

    def __attrs_post_init__(self) -> None:
        self._draw_pile = Deck._init_draw_pile()
        self._discard_pile = {}

    @staticmethod
    def _init_draw_pile() -> Dict[int, Card]:
        pile = {}
        cardid = 0
        for card in CardType:
            for _ in range(DECK_COUNTS[card]):
                pile[cardid] = Card(cardid, card)
                cardid += 1
        return pile

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

    Attributes:
        color(str): The color of this pawn
        index(int): Zero-based index of this pawn for a given user
        name(str): The full name of this pawn as "color-index"
        start(boolean): Whether this pawn resides in its start area
        home(boolean): Whether this pawn resides in its home area
        safe(int): Zero-based index of the square in the safe area where this pawn resides
        square(int): Zero-based index of the square on the board where this pawn resides
    """

    color = attr.ib(type=str)
    index = attr.ib(type=int)
    name = attr.ib(type=str)
    start = attr.ib(init=False, default=True)
    home = attr.ib(init=False, default=False)
    safe = attr.ib(init=False, default=None, type=Optional[int])
    square = attr.ib(init=False, default=None, type=Optional[int])

    @name.default
    def _default_name(self) -> str:
        return "%s-%s" % (self.color, self.index)

    def move_to_start(self) -> None:
        """Move to the pawn to its start area."""
        self.start = True
        self.home = False
        self.safe = None
        self.square = None

    def move_to_home(self) -> None:
        """Move to the pawn to its home area."""
        self.start = False
        self.home = True
        self.safe = None
        self.square = None

    def move_to_safe(self, square: int) -> None:
        """
        Move to the pawn to a square in its safe area.

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
        Move to the pawn to a square on the board.

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

    Attributes:
        color(str): The color of the player
        hand(:obj:`list` of :obj:`Card`): List of cards in the player's hand
        pawns(:obj:`list` of :obj:`Pawn`): List of all pawns belonging to the player
    """

    color = attr.ib(type=str)
    hand = attr.ib(init=False, type=List[Card])
    pawns = attr.ib(init=False, type=List[Pawn])

    def __attrs_post_init__(self) -> None:
        self.hand = []
        self.pawns = [Pawn(self.color, index) for index in range(0, PAWNS)]


@attr.s
class Game:
    """
    The game, consisting of state for a set of players.

    Attributes:
        playercount(int): Number of players in the game
        players(:obj:`dict` of :obj:`Player`): All players in the game
        deck(Deck): The deck of cards for the game
    """

    playercount = attr.ib(type=int)
    players = attr.ib(init=False, type=Dict[str, Player])
    deck = attr.ib(init=False, type=Deck)
    _started = attr.ib(init=False, default=False, type=bool)
    _adult_mode = attr.ib(init=False, default=False, type=bool)

    @playercount.validator
    def _check_playercount(self, attribute: str, value: int) -> None:
        if value < MIN_PLAYERS or value > MAX_PLAYERS:
            raise ValueError("Invalid number of players")

    def __attrs_post_init__(self) -> None:
        self.players = {color: Player(color) for color in PLAYER_COLORS[: self.playercount]}
        self.deck = Deck()

    @property
    def started(self) -> bool:
        return self._started

    @property
    def adult_mode(self) -> bool:
        return self._adult_mode

    def set_adult_mode(self) -> None:
        """Set adult mode for the game."""
        if self._started:
            raise ValueError("Game is already started; mode cannot be changed")
        self._adult_mode = True
        for player in self.players.values():
            player.pawns[0].move_to_start()
        for _ in range(ADULT_HAND):
            for player in self.players.values():
                player.hand.append(self.deck.draw())
