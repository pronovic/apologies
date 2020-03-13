# -*- coding: utf-8 -*-
# vim: set ft=python ts=3 sw=3 expandtab:

# A game consists of 2-4 players
MIN_PLAYERS = 2
MAX_PLAYERS = 4

# Each player gets one color
RED = "RED"
BLUE = "BLUE"
YELLOW = "YELLOW"
GREEN = "GREEN"
COLORS = [ RED, YELLOW, GREEN, BLUE, ]  # order chosen so game works better for < 4 players

# There are 4 pieces per player
PIECES = 4

# There are 60 squares around the outside of the board
BOARD_SQUARES = 60

# There are 5 safe squares for each color
SAFE_SQUARES = 5

# A piece on the board, belonging to a player
class Piece:
   def __init__(self, color, index):
      self.color = color
      self.index = index
      self.name = "%s-%s" % (color, index)
      self.start = True    # whether this piece resides in the start area
      self.home = False    # whether this piece resides in in the home area
      self.safe = None     # zero-based index of the square in the safe area where this piece resides
      self.square = None   # zero-based index of the square on the board where this piece resides

   def __repr__(self):
      return "Piece(name=%s, start=%s, home=%s, safe=%s, square=%s)" % (self.name, self.start, self.home, self.safe, self.square)

   def move_to_start(self):
      self.start = True
      self.home = False
      self.safe = None
      self.square = None

   def move_to_home(self):
      self.start = False
      self.home = True
      self.safe = None
      self.square = None

   def move_to_safe(self, square):
      if not square in range(SAFE_SQUARES): raise ValueError("Invalid square")
      self.start = False
      self.home = False
      self.safe = square
      self.square = None

   def move_to_square(self, square):
      if not square in range(BOARD_SQUARES): raise ValueError("Invalid square")
      self.start = False
      self.home = False
      self.safe = None
      self.square = square

# All of the pieces belonging to a player
class Pieces(list):
   def __init__(self, color):
      self.color = color
      for index in range(0, PIECES):
         self.append(Piece(color, index))

# A player, which has a color and 4 pieces
class Player:
   def __init__(self, color, name=None):
      self.color = color
      self.name = name
      self.pieces = Pieces(color)

   def __repr__(self):
      return "Player(%s, %s): %s" % (self.color, self.name, self.pieces)
   

# All of the players in the game
class Players(dict):
   def __init__(self, players):
      if players < MIN_PLAYERS or players > MAX_PLAYERS: raise ValueError("Invalid number of players")
      for color in COLORS[:players]:
         self[color] = Player(color)

   def __iter__(self):
      return (player for player in self.values())

# The game, consisting of state for a set of players
class Game:
   def __init__(self, players=MAX_PLAYERS):
      self.players = Players(players)
   
   def __str__(self):
      return "Game(players=%s)" % self.players
