# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access

import pytest
from flexmock import flexmock

from apologies.game import ADULT_HAND, DECK_SIZE, Card, CardType, Game, GameMode, Pawn, PlayerColor
from apologies.rules import Action, ActionType, Move, Rules


class TestAction:
    def test_move_from_start(self):
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(ActionType.MOVE_FROM_START, mine=mine)
        assert action.actiontype == ActionType.MOVE_FROM_START
        assert action.mine is mine
        assert action.theirs is None
        assert action.squares is None

    def test_move_forward(self):
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(actiontype=ActionType.MOVE_FORWARD, mine=mine, squares=5)
        assert action.actiontype == ActionType.MOVE_FORWARD
        assert action.mine is mine
        assert action.theirs is None
        assert action.squares == 5

    def test_move_backward(self):
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(actiontype=ActionType.MOVE_BACKARD, mine=mine, squares=5)
        assert action.actiontype == ActionType.MOVE_BACKARD
        assert action.mine is mine
        assert action.theirs is None
        assert action.squares == 5

    def test_change_places(self):
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        theirs = Pawn(PlayerColor.BLUE, 2, "theirs")
        action = Action(actiontype=ActionType.CHANGE_PLACES, mine=mine, theirs=theirs, squares=5)
        assert action.actiontype == ActionType.CHANGE_PLACES
        assert action.mine is mine
        assert action.theirs is theirs
        assert action.squares == 5

    def test_bump_to_start(self):
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        theirs = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(actiontype=ActionType.BUMP_TO_START, mine=mine, theirs=theirs)
        assert action.actiontype == ActionType.BUMP_TO_START
        assert action.mine is mine
        assert action.theirs is theirs
        assert action.squares is None


class TestMove:
    def test_constructor(self):
        card = Card(3, CardType.CARD_12)
        actions = [Action(ActionType.MOVE_FROM_START, mine=Pawn(PlayerColor.BLUE, 1, "whatever"))]
        move = Move(card, actions)
        assert move.card is card
        assert move.actions == actions


class TestRules:
    def test_constructor(self):
        rules = Rules(GameMode.STANDARD)
        assert rules.mode == GameMode.STANDARD

    def test_draw_again(self):
        rules = Rules(GameMode.STANDARD)
        for cardtype in CardType:
            if cardtype == CardType.CARD_2:
                assert rules.draw_again(Card(0, cardtype)) is True
            else:
                assert rules.draw_again(Card(0, cardtype)) is False

    def test_start_game_started(self):
        game = flexmock(started=True)
        rules = Rules(GameMode.STANDARD)
        with pytest.raises(ValueError):
            rules.start_game(game)

    def test_start_game_standard(self):
        game = Game(2)
        rules = Rules(GameMode.STANDARD)
        rules.start_game(game)

        assert game.started is True
        assert len(game.deck._draw_pile) == DECK_SIZE

        for color in [PlayerColor.RED, PlayerColor.YELLOW]:
            assert game.players[color].color == color
            assert len(game.players[color].hand) == 0

    def test_start_game_adult(self):
        game = Game(4)
        rules = Rules(GameMode.ADULT)
        rules.start_game(game)

        assert game.started is True
        assert len(game.deck._draw_pile) == DECK_SIZE - (4 * ADULT_HAND)

        assert game.players[PlayerColor.RED].color == PlayerColor.RED
        assert game.players[PlayerColor.RED].pawns[0].square == 4
        assert len(game.players[PlayerColor.RED].hand) == ADULT_HAND

        assert game.players[PlayerColor.YELLOW].color == PlayerColor.YELLOW
        assert game.players[PlayerColor.YELLOW].pawns[0].square == 34
        assert len(game.players[PlayerColor.YELLOW].hand) == ADULT_HAND

        assert game.players[PlayerColor.GREEN].color == PlayerColor.GREEN
        assert game.players[PlayerColor.GREEN].pawns[0].square == 49
        assert len(game.players[PlayerColor.GREEN].hand) == ADULT_HAND

        assert game.players[PlayerColor.BLUE].color == PlayerColor.BLUE
        assert game.players[PlayerColor.BLUE].pawns[0].square == 19
        assert len(game.players[PlayerColor.BLUE].hand) == ADULT_HAND

    def test_execute_move(self):
        # TODO: there will be a zillion of these methods for various kinds of moves
        pytest.fail("Not implemented")
