# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Classes that track game state.

Note that these classes track game state, but do not implement game rules.  The
only validations are to prevent changes that literally cannot be represented in
game state, such as selecting an invalid square.  All other rules (such as the
restriction that only one pawn can occupy a space, or the act of sliding down a
slider, etc.) are implemented elsewhere, using the methods available on these
classes.

Attributes:
    MIN_PLAYERS(int): Minimum number of players in a game
    MAX_PLAYERS(int): Maximum number of players in a game
    RED(str): The red player color
    BLUE(str): The blue player color
    YELLOW(str): The yellow player color
    GREEN(str): The green player color
    COLORS(list): All available player colors, listed in order of use
    PAWNS(int): Number of pawns per player
    SAFE_SQUARES(int): Number of safe squares for each color
    BOARD_SQUARES(int): Number of squares around the outside of the board
"""

import attr

# A game consists of 2-4 players
MIN_PLAYERS = 2
MAX_PLAYERS = 4

# Each player gets one color
RED = "RED"
BLUE = "BLUE"
YELLOW = "YELLOW"
GREEN = "GREEN"
COLORS = [RED, YELLOW, GREEN, BLUE]  # order chosen so game works better for < 4 players

# There are 4 pawns per player, numbered 0-3
PAWNS = 4

# There are 5 safe squares for each color, numbered 0-4
SAFE_SQUARES = 5

# There are 60 squares around the outside of the board, numbered 0-59
BOARD_SQUARES = 60


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

    color = attr.ib()
    index = attr.ib()
    name = attr.ib()
    start = attr.ib(init=False, default=True)
    home = attr.ib(init=False, default=False)
    safe = attr.ib(init=False, default=None)
    square = attr.ib(init=False, default=None)

    @name.default
    def _default_name(self):
        return "%s-%s" % (self.color, self.index)

    def move_to_start(self):
        """
        Move to the pawn to its start area.
        """

        self.start = True
        self.home = False
        self.safe = None
        self.square = None

    def move_to_home(self):
        """
        Move to the pawn to its home area.
        """

        self.start = False
        self.home = True
        self.safe = None
        self.square = None

    def move_to_safe(self, square):
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

    def move_to_square(self, square):
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
        name(str, optional): The name of the player
        pawns(Pawns): List of all pawns belonging to the player
    """

    color = attr.ib()
    name = attr.ib(default=None)
    pawns = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.pawns = [Pawn(self.color, index) for index in range(0, PAWNS)]


@attr.s
class Game:
    """
    The game, consisting of state for a set of players.

    Attributes:
        playercount(int): Number of players in the game
        players(:obj:`dict` of :obj:`Player`): A dict containing all players in the game.
    """

    playercount = attr.ib()
    players = attr.ib(init=False)

    @playercount.validator
    def _check_playercount(self, attribute, value):
        if value < MIN_PLAYERS or value > MAX_PLAYERS:
            raise ValueError("Invalid number of players")

    def __attrs_post_init__(self):
        self.players = {color: Player(color) for color in COLORS[: self.playercount]}
