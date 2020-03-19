# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=wildcard-import,no-self-use,protected-access
# Unit tests for game.py

from flexmock import flexmock
from apologies.game import Pawn, Card, CardType, PlayerColor
from apologies.character import *


class TestMoveFromStartAction:
    def test_constructor(self) -> None:
        MoveFromStartAction()  # just make sure it can be built


class TestMoveForwardAction:
    def test_constructor(self) -> None:
        pawn = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = MoveForwardAction(pawn, 5)
        assert action.pawn is pawn
        assert action.spaces == 5


class TestMoveBackwardAction:
    def test_constructor(self) -> None:
        pawn = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = MoveBackwardAction(pawn, 5)
        assert action.pawn is pawn
        assert action.spaces == 5


class TestChangePlacesAction:
    def test_constructor(self) -> None:
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        theirs = Pawn(PlayerColor.BLUE, 2, "theirs")
        action = ChangePlacesAction(mine, theirs)
        assert action.mine is mine
        assert action.theirs is theirs


class TestBumpToStartAction:
    def test_constructor(self) -> None:
        bumped = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = BumpToStartAction(bumped)
        assert action.bumped is bumped


class TestMove:
    def test_constructor(self) -> None:
        card = Card(3, CardType.CARD_12)
        actions = [MoveFromStartAction()]
        move = Move(card, actions)
        assert move.card is card
        assert move.actions == actions


class TestCharacter:
    def test_constructor(self) -> None:
        game = flexmock()
        player = flexmock()
        source = flexmock()
        character = Character("c", game, player, source)
        assert character.name == "c"
        assert character.game is game
        assert character.player is player
        assert character.source is source

    def test_construct_move_no_card(self) -> None:
        game = flexmock()
        player = flexmock()
        source = flexmock()
        character = Character("c", game, player, source)
        flexmock(source).should_receive("construct_move").with_args(game, player, None).once()
        character.construct_move()

    def test_construct_move_with_card(self) -> None:
        game = flexmock()
        player = flexmock()
        source = flexmock()
        card = flexmock()
        character = Character("c", game, player, source)
        flexmock(source).should_receive("construct_move").with_args(game, player, card).once()
        character.construct_move(card)
