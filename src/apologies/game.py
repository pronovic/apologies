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

from collections import OrderedDict

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

    def __init__(self, color, index):
        """
        Create a pawn.

        Args:
            color(str): The color of this pawn
            index(int): Zero-based index of this pawn for a given user
        """
        self.color = color
        self.index = index
        self.name = "%s-%s" % (color, index)
        self.start = True
        self.home = False
        self.safe = None
        self.square = None

    def __repr__(self):
        return "Pawn(name=%s, start=%s, home=%s, safe=%s, square=%s)" % (
            self.name,
            self.start,
            self.home,
            self.safe,
            self.square,
        )

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

        if not square in range(SAFE_SQUARES):
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

        if not square in range(BOARD_SQUARES):
            raise ValueError("Invalid square")
        self.start = False
        self.home = False
        self.safe = None
        self.square = square


class Pawns(list):
    """
    A list of all pawns belonging to a player.

    Attributes:
        color(str): The color of the pawns
    """

    def __init__(self, color):
        """
        Create a complete set of pawns.

        Args:
            color(str): The color of the pawns
        """
        super(Pawns, self).__init__()
        self.color = color
        for index in range(0, PAWNS):
            self.append(Pawn(color, index))


class Player:
    """
    A player, which has a color and a set of pawns.

    Attributes:
        color(str): The color of the player
        name(str, optional): The name of the player
        pawns(Pawns): List of all pawns belonging to the player
    """

    def __init__(self, color, name=None):
        """
        Create a player.

        Args:
            color(str): The color of the player
            name(str, optional): The name of the player
        """
        self.color = color
        self.name = name
        self.pawns = Pawns(color)

    def __repr__(self):
        return "Player(%s, %s): %s" % (self.color, self.name, self.pawns)


class Players(OrderedDict):
    """
    A dict containing all players in the game.
    """

    def __init__(self, players):
        """
        Create players, allocated out of COLORS in order.

        Args:
            players(int): The number of players in the game
        """
        super(Players, self).__init__()
        if players < MIN_PLAYERS or players > MAX_PLAYERS:
            raise ValueError("Invalid number of players")
        for color in COLORS[:players]:
            self[color] = Player(color)

    def __iter__(self):
        return (player for player in self.values())


class Game:
    """
    The game, consisting of state for a set of players.

    Attributes:
        players(Players): A dict containing all players in the game.
    """

    def __init__(self, players=MAX_PLAYERS):
        """
        Create a new game.

        Args:
            players(int, optional): The number of players in the game
        """
        self.players = Players(players)

    def __str__(self):
        return "Game(players=%s)" % self.players
