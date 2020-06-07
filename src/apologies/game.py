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
    DECK_COUNTS(Dict[Card, int]): Dictionary from card name to number of cards in a standard deck
    DECK_SIZE(int): The total expected size of a complete deck
    DRAW_AGAIN(Dict[Card, bool]): Whether each card results in a draw again action
    CIRCLE(Dict[PlayerColor, Position]): The position of the start circle for each color
    TURN(Dict[PlayerColor, Position()): The position of the turn square for each color, where forward movement turns into safe zone
    SLIDE(Dict[PlayerColor, Tuple(int, int)): The slide start/end squares for each color
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

# Cattr converter that serializes/deserializes DateTime to an ISO 8601 timestamp
_CONVERTER = CattrConverter()

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
    """
    All legal types of cards.

    The "A" card (CARD_APOLOGIES) is like the "Sorry" card in the original game.
    """

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
    CARD_APOLOGIES = "A"  # This is like the "Sorry" card in the original game


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

# Whether a card draws again
DRAW_AGAIN = {
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
    def _default_draw_pile(self) -> Dict[str, Card]:
        pile = {}
        cardid = 0
        for card in CardType:
            for _ in range(DECK_COUNTS[card]):
                pile["%d" % cardid] = Card("%d" % cardid, card)
                cardid += 1
        return pile

    @_discard_pile.default
    def _default_discard_pile(self) -> Dict[str, Card]:
        return {}

    def draw(self) -> Card:
        """Draw a random card from the draw pile."""
        if len(self._draw_pile) < 1:
            # this is equivalent to shuffling the discard pile into the draw pile
            for card in list(self._discard_pile.values()):
                self._discard_pile.pop(card.id)
                self._draw_pile[card.id] = card
        if len(self._draw_pile) < 1:
            raise ValueError("No cards available in deck")  # in any normal game, this should never happen
        return self._draw_pile.pop(random.choice(list(self._draw_pile.keys())))

    def discard(self, card: Card) -> None:
        """Discard back to the discard pile."""
        if card.id in self._draw_pile or card.id in self._discard_pile:
            raise ValueError("Card already exists in deck")
        self._discard_pile[card.id] = card


@attr.s
class Position:
    """
    The position of a pawn on the board.

    Callers should not pass in or directly modify the start, home, safe, or square
    attributes.  These are accessible to support serialization and deserialization.
    Instead, use the provided methods to safely modify the object in-place.

    Attributes:
        start(boolean): Whether this pawn resides in its start area
        home(boolean): Whether this pawn resides in its home area
        safe(int): Zero-based index of the square in the safe area where this pawn resides
        square(int): Zero-based index of the square on the board where this pawn resides
    """

    start = attr.ib(default=True, type=bool)
    home = attr.ib(default=False, type=bool)
    safe = attr.ib(default=None, type=Optional[int])
    square = attr.ib(default=None, type=Optional[int])

    def __str__(self) -> str:
        if self.home:
            return "home"
        elif self.start:
            return "start"
        elif self.safe is not None:
            return "safe %s" % self.safe
        else:
            return "square %s" % self.square

    def copy(self) -> Position:
        """Return a fully-independent copy of the position."""
        return _CONVERTER.structure(_CONVERTER.unstructure(self), Position)  # type: ignore

    def move_to_position(self, position: Position) -> Position:
        """
        Move the pawn to a specific position on the board.

        Returns:
            Position: A reference to the position, for chaining
            
        Raises:
            ValueError: If the position is invalid
        """
        fields = 0
        if position.start:
            fields += 1
        if position.home:
            fields += 1
        if position.safe is not None:
            fields += 1
        if position.square is not None:
            fields += 1
        if fields != 1:
            raise ValueError("Invalid position")
        if position.start:
            self.move_to_start()
        elif position.home:
            self.move_to_home()
        elif position.safe is not None:
            self.move_to_safe(position.safe)
        elif position.square is not None:
            self.move_to_square(position.square)
        return self

    def move_to_start(self) -> Position:
        """
        Move the pawn back to its start area.

        Returns:
            Position: A reference to the position, for chaining
            
        Raises:
            ValueError: If the position is invalid
        """
        self.start = True
        self.home = False
        self.safe = None
        self.square = None
        return self

    def move_to_home(self) -> Position:
        """
        Move the pawn to its home area.

        Returns:
            Position: A reference to the position, for chaining
            
        Raises:
            ValueError: If the position is invalid
        """
        self.start = False
        self.home = True
        self.safe = None
        self.square = None
        return self

    def move_to_safe(self, square: int) -> Position:
        """
        Move the pawn to a square in its safe area.

        Args:
            square(int): Zero-based index of the square in the safe area

        Returns:
            Position: A reference to the position, for chaining

        Raises:
            ValueError: If the square is not valid
        """
        if square not in range(SAFE_SQUARES):
            raise ValueError("Invalid square")
        self.start = False
        self.home = False
        self.safe = square
        self.square = None
        return self

    def move_to_square(self, square: int) -> Position:
        """
        Move the pawn to a square on the board.

        Args:
            square(int): Zero-based index of the square on the board where this pawn resides

        Returns:
            Position: A reference to the position, for chaining

        Raises:
            ValueError: If the square is not valid
        """
        if square not in range(BOARD_SQUARES):
            raise ValueError("Invalid square")
        self.start = False
        self.home = False
        self.safe = None
        self.square = square
        return self


@attr.s
class Pawn:
    """
    A pawn on the board, belonging to a player.

    Callers should not pass in the position attribute.  This is accessible
    to support serialization and deserialization. Instead, use the provided
    methods to safely modify the position in-place.

    Attributes:
        color(str): The color of this pawn
        index(int): Zero-based index of this pawn for a given user
        name(str): The full name of this pawn as "colorindex"
        position(Position): The position of this pawn on the board
    """

    color = attr.ib(type=PlayerColor)
    index = attr.ib(type=int)
    name = attr.ib(type=str)
    position = attr.ib(type=Position)

    @name.default
    def _default_name(self) -> str:
        return "%s%s" % (self.color.value, self.index)

    @position.default
    def _default_position(self) -> Position:
        return Position()

    def __str__(self) -> str:
        return "%s->%s" % (self.name, self.position)


@attr.s
class Player:
    """
    A player, which has a color and a set of pawns.

    Callers should not pass in the hand and pawns constructor arguments.  These
    are accessible to support serialization and deserialization.

    Attributes:
        color(str): The color of the player
        hand(List[Card]): List of cards in the player's hand
        pawns(List[Pawn]): List of all pawns belonging to the player
        turns(int): Number of turns for this player
    """

    color = attr.ib(type=PlayerColor)
    hand = attr.ib(type=List[Card])
    pawns = attr.ib(type=List[Pawn])
    turns = attr.ib(type=int, default=0)

    @hand.default
    def _default_hand(self) -> List[Card]:
        return []

    @pawns.default
    def _default_pawns(self) -> List[Pawn]:
        return [Pawn(self.color, index) for index in range(0, PAWNS)]

    def copy(self) -> Player:
        """Return a fully-independent copy of the player."""
        return _CONVERTER.structure(_CONVERTER.unstructure(self), Player)  # type: ignore

    def public_data(self) -> Player:
        """Return a fully-independent copy of the player with only public data visible."""
        player = self.copy()
        del player.hand[:]  # other players should not see this player's hand when making decisions
        return player

    def find_first_pawn_in_start(self) -> Optional[Pawn]:
        """Find the first pawn in the start area, if any."""
        for pawn in self.pawns:
            if pawn.position.start:
                return pawn
        return None

    def all_pawns_in_home(self) -> bool:
        """Whether all of this user's pawns are in home."""
        for pawn in self.pawns:
            if not pawn.position.home:
                return False
        return True


@attr.s
class History:
    """
    Tracks an action taken during the game.

    Attributes:
        action(str): String describing the action
        color(Optional[PlayerColor]): Color of the player associated with the action
        card(Optional[CardType]): Card associated with the action
        timestamp(DateTime): Timestamp tied to the action (defaults to current time)
    """

    action = attr.ib(type=str)
    color = attr.ib(default=None, type=Optional[PlayerColor])
    card = attr.ib(default=None, type=Optional[CardType])
    timestamp = attr.ib(type=DateTime)

    @timestamp.default
    def _default_timestamp(self) -> DateTime:
        return pendulum.now(pendulum.UTC)

    def __str__(self) -> str:
        time = self.timestamp.to_time_string()  # type: ignore
        color = "General" if not self.color else self.color.value
        action = self.action
        return "[%s] %s - %s" % (time, color, action)


@attr.s
class PlayerView:
    """
    A player-specific view of the game, showing only the information a player would have available on their turn.
      
    Attributes:
        player(Player): The player associated with the view.
        opponents(Dict[PlayerColor, Player]): The player's opponents, with private information stripped
    """

    player = attr.ib(type=Player)
    opponents = attr.ib(type=Dict[PlayerColor, Player])

    def copy(self) -> PlayerView:
        """Return a fully-independent copy of the player view."""
        return _CONVERTER.structure(_CONVERTER.unstructure(self), PlayerView)  # type: ignore

    def get_pawn(self, prototype: Pawn) -> Optional[Pawn]:
        """Return the pawn from this view with the same color and index."""
        for pawn in self.all_pawns():
            if pawn.color == prototype.color and pawn.index == prototype.index:
                return pawn
        return None

    def all_pawns(self) -> List[Pawn]:
        """Return a list of all pawns on the board."""
        pawns = []
        pawns.extend(self.player.pawns)
        for opponent in self.opponents.values():
            pawns.extend(opponent.pawns)
        return pawns


@attr.s
class Game:
    """
    The game, consisting of state for a set of players.

    Callers should not pass in optional constructor arguments.  These are accessible
    to support serialization and deserialization.

    Attributes:
        playercount(int): Number of players in the game
        players(Dict[PlayerColor, Player]): All players in the game
        deck(Deck): The deck of cards for the game
    """

    playercount = attr.ib(type=int)
    players = attr.ib(type=Dict[PlayerColor, Player])
    deck = attr.ib(type=Deck)
    history = attr.ib(type=List[History])

    @playercount.validator
    def _check_playercount(self, _attribute: str, value: int) -> None:
        if value < MIN_PLAYERS or value > MAX_PLAYERS:
            raise ValueError("Invalid number of players")

    @players.default
    def _default_players(self) -> Dict[PlayerColor, Player]:
        return {color: Player(color) for color in list(PlayerColor)[: self.playercount]}

    @deck.default
    def _default_deck(self) -> Deck:
        return Deck()

    @history.default
    def _default_history(self) -> List[History]:
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

    @property
    def winner(self) -> Optional[Player]:
        """The winner of the game, if any."""
        for player in self.players.values():
            if player.all_pawns_in_home():
                return player
        return None

    def copy(self) -> Game:
        """Return a fully-independent copy of the game."""
        return _CONVERTER.structure(_CONVERTER.unstructure(self), Game)  # type: ignore

    def to_json(self) -> str:
        """Serialize the game state to JSON."""
        return orjson.dumps(_CONVERTER.unstructure(self), option=orjson.OPT_INDENT_2).decode("utf-8")  # type: ignore

    @staticmethod
    def from_json(data: str) -> Game:
        """Deserialize the game state from JSON."""
        return _CONVERTER.structure(orjson.loads(data), Game)  # type: ignore

    def track(self, action: str, player: Optional[Player] = None, card: Optional[Card] = None) -> None:
        """Tracks an action taken during the game."""
        self.history.append(History(action, player.color if player else None, card.cardtype if card else None))
        if player:
            self.players[player.color].turns += 1

    def create_player_view(self, color: PlayerColor) -> PlayerView:
        """Return a player-specific view of the game, showing only the information a player would have available on their turn."""
        player = self.players[color].copy()
        opponents = {player.color: player.public_data() for player in self.players.values() if player.color != color}
        return PlayerView(player, opponents)


# The start circles for each color
CIRCLE = {
    PlayerColor.RED: Position().move_to_square(4),
    PlayerColor.BLUE: Position().move_to_square(19),
    PlayerColor.YELLOW: Position().move_to_square(34),
    PlayerColor.GREEN: Position().move_to_square(49),
}

# The turn squares for each color, where forward movement turns into the safe zone
TURN = {
    PlayerColor.RED: Position().move_to_square(2),
    PlayerColor.BLUE: Position().move_to_square(17),
    PlayerColor.YELLOW: Position().move_to_square(32),
    PlayerColor.GREEN: Position().move_to_square(47),
}

# The slide start/end positions for each color
SLIDE = {
    PlayerColor.RED: ((1, 4), (9, 13)),
    PlayerColor.BLUE: ((16, 19), (24, 28)),
    PlayerColor.YELLOW: ((31, 34), (39, 43)),
    PlayerColor.GREEN: ((46, 49), (54, 58)),
}
