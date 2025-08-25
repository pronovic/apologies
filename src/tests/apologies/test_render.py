# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name

import os

import pytest

from apologies.game import Game, PlayerColor
from apologies.render import render_board

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures/test_render")


@pytest.fixture
def data():
    data = {}
    for f in os.listdir(FIXTURE_DIR):
        p = os.path.join(FIXTURE_DIR, f)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as r:
                data[f] = r.read()
    return data


# Unit tests for render_board()
class TestRenderBoard:
    def test_empty_2_player_empty(self, data):
        game = Game(playercount=2)
        expected = data["empty2"]
        actual = render_board(game)
        assert expected == actual

    def test_empty_3_player_empty(self, data):
        game = Game(playercount=3)
        expected = data["empty3"]
        actual = render_board(game)
        assert expected == actual

    def test_empty_4_player_empty(self, data):
        game = Game(playercount=4)
        expected = data["empty4"]
        actual = render_board(game)
        assert expected == actual

    def test_home(self, data):
        game = _fill_home()
        expected = data["home"]
        actual = render_board(game)
        assert expected == actual

    def test_safe_03(self, data):
        game = _fill_safe(0)
        expected = data["safe_03"]
        actual = render_board(game)
        assert expected == actual

    def test_safe_14(self, data):
        game = _fill_safe(1)
        expected = data["safe_14"]
        actual = render_board(game)
        assert expected == actual

    def test_top(self, data):
        game = _fill_squares(0, 15)
        expected = data["top"]
        actual = render_board(game)
        assert expected == actual

    def test_right(self, data):
        game = _fill_squares(16, 29)
        expected = data["right"]
        actual = render_board(game)
        assert expected == actual

    def test_bottom(self, data):
        game = _fill_squares(30, 45)
        expected = data["bottom"]
        actual = render_board(game)
        assert expected == actual

    def test_left(self, data):
        game = _fill_squares(46, 59)
        expected = data["left"]
        actual = render_board(game)
        assert expected == actual


# Create a game with all players in home
def _fill_home() -> Game:
    game = Game(playercount=4)
    for color in [PlayerColor.BLUE, PlayerColor.RED, PlayerColor.YELLOW, PlayerColor.GREEN]:
        for pawn in range(4):
            game.players[color].pawns[pawn].position.move_to_home()
    return game


# Create a game with all players in the safe zone
def _fill_safe(start: int) -> Game:
    game = Game(playercount=4)
    for color in [PlayerColor.BLUE, PlayerColor.RED, PlayerColor.YELLOW, PlayerColor.GREEN]:
        for pawn in range(4):
            game.players[color].pawns[pawn].position.move_to_safe(pawn + start)
    return game


# Fill a range of squares on the board with pieces from various players
def _fill_squares(start: int, end: int) -> Game:
    game = Game(playercount=4)
    square = 0
    for pawn in range(4):
        for color in [PlayerColor.BLUE, PlayerColor.RED, PlayerColor.YELLOW, PlayerColor.GREEN]:
            if square + start <= end:
                game.players[color].pawns[pawn].position.move_to_square(square + start)
                square += 1
    return game
