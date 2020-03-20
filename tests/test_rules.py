# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access

from flexmock import flexmock

from apologies.character import Character
from apologies.game import Card, CardType, Pawn, PlayerColor
from apologies.rules import Action, ActionType, Move


class TestAction:
    def test_move_from_start(self) -> None:
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(ActionType.MOVE_FROM_START, mine=mine)
        assert action.actiontype == ActionType.MOVE_FROM_START
        assert action.mine is mine
        assert action.theirs is None
        assert action.squares is None

    def test_move_forward(self) -> None:
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(actiontype=ActionType.MOVE_FORWARD, mine=mine, squares=5)
        assert action.actiontype == ActionType.MOVE_FORWARD
        assert action.mine is mine
        assert action.theirs is None
        assert action.squares == 5

    def test_move_backward(self) -> None:
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(actiontype=ActionType.MOVE_BACKARD, mine=mine, squares=5)
        assert action.actiontype == ActionType.MOVE_BACKARD
        assert action.mine is mine
        assert action.theirs is None
        assert action.squares == 5

    def test_change_places(self) -> None:
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        theirs = Pawn(PlayerColor.BLUE, 2, "theirs")
        action = Action(actiontype=ActionType.CHANGE_PLACES, mine=mine, theirs=theirs, squares=5)
        assert action.actiontype == ActionType.CHANGE_PLACES
        assert action.mine is mine
        assert action.theirs is theirs
        assert action.squares == 5

    def test_bump_to_start(self) -> None:
        mine = Pawn(PlayerColor.BLUE, 1, "whatever")
        theirs = Pawn(PlayerColor.BLUE, 1, "whatever")
        action = Action(actiontype=ActionType.BUMP_TO_START, mine=mine, theirs=theirs)
        assert action.actiontype == ActionType.BUMP_TO_START
        assert action.mine is mine
        assert action.theirs is theirs
        assert action.squares is None


class TestMove:
    def test_constructor(self) -> None:
        card = Card(3, CardType.CARD_12)
        actions = [Action(ActionType.MOVE_FROM_START, mine=Pawn(PlayerColor.BLUE, 1, "whatever"))]
        move = Move(card, actions)
        assert move.card is card
        assert move.actions == actions


class TestCharacter:
    def test_constructor(self) -> None:
        source = flexmock()
        character = Character("c", source)
        assert character.name == "c"
        assert character.source is source

    def test_construct_move_minimal(self) -> None:
        source = flexmock()
        character = Character("c", source)
        game = flexmock()
        mode = flexmock()
        player = flexmock()
        flexmock(source).should_receive("construct_move").with_args(game, mode, player, None, False).once()
        character.construct_move(game, mode, player)

    def test_construct_move_all_args(self) -> None:
        source = flexmock()
        character = Character("c", source)
        game = flexmock()
        mode = flexmock()
        player = flexmock()
        card = flexmock()
        flexmock(source).should_receive("construct_move").with_args(game, mode, player, card, True).once()
        character.construct_move(game, mode, player, card, True)
