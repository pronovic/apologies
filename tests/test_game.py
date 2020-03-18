# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=wildcard-import,no-self-use
# Unit tests for game.py

import pytest
from apologies.game import *

# Unit tests for Pawn
class TestPawn:
    def test_constructor(self):
        pawn = Pawn("color", 0)
        assert pawn.color == "color"
        assert pawn.index == 0
        assert pawn.name == "color-0"
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_constructor_with_name(self):
        pawn = Pawn("color", 0, name="whatever")
        assert pawn.color == "color"
        assert pawn.index == 0
        assert pawn.name == "whatever"
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_start(self):
        pawn = Pawn("color", 0)
        pawn.start = "x"
        pawn.home = "x"
        pawn.safe = "x"
        pawn.square = "x"
        pawn.move_to_start()
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_home(self):
        pawn = Pawn("color", 0)
        pawn.start = "x"
        pawn.home = "x"
        pawn.safe = "x"
        pawn.square = "x"
        pawn.move_to_home()
        assert pawn.start is False
        assert pawn.home is True
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_safe_valid(self):
        for square in range(SAFE_SQUARES):
            pawn = Pawn("color", 0)
            pawn.start = "x"
            pawn.home = "x"
            pawn.safe = "x"
            pawn.square = "x"
            pawn.move_to_safe(square)
            assert pawn.start is False
            assert pawn.home is False
            assert pawn.safe == square
            assert pawn.square is None

    def test_move_to_safe_invalid(self):
        for square in [-1000, -2 - 1, 5, 6, 1000]:
            with pytest.raises(ValueError):
                pawn = Pawn("color", 0)
                pawn.move_to_safe(square)

    def test_move_to_square_invalid(self):
        for square in [-1000, -2 - 1, 60, 61, 1000]:
            with pytest.raises(ValueError):
                pawn = Pawn("color", 0)
                pawn.move_to_square(square)


# Unit tests for Player
class TestPlayer:
    def test_constructor(self):
        player = Player("color")
        assert player.color == "color"
        assert player.name is None
        assert len(player.pawns) == PAWNS
        for pawn in player.pawns:
            assert isinstance(pawn, Pawn)


# Unit tests for Game
class TestGame:
    def test_constructor_2_players(self):
        game = Game(2)
        assert len(game.players) == 2
        assert game.players[RED].color == RED
        assert game.players[YELLOW].color == YELLOW

    def test_constructor_3_players(self):
        game = Game(3)
        assert len(game.players) == 3
        assert game.players[RED].color == RED
        assert game.players[YELLOW].color == YELLOW
        assert game.players[GREEN].color == GREEN

    def test_constructor_4_players(self):
        game = Game(4)
        assert len(game.players) == 4
        assert game.players[RED].color == RED
        assert game.players[YELLOW].color == YELLOW
        assert game.players[GREEN].color == GREEN
        assert game.players[BLUE].color == BLUE

    def test_constructor_invalid_players(self):
        for playercount in [-2, -1, 0, 1, 5, 6]:
            with pytest.raises(ValueError):
                Game(playercount)
