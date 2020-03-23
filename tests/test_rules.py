# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access,too-many-locals

import pytest
from mock import MagicMock, Mock, call

from apologies.game import ADULT_HAND, DECK_SIZE, Card, CardType, Game, GameMode, Pawn, PlayerColor
from apologies.rules import Action, ActionType, BoardRules, Move, Rules


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


class TestBoardRules:
    def test_construct_legal_moves(self):
        # TODO: test real implementation
        card = Mock()
        pawn = Mock()
        all_pawns = []
        assert BoardRules.construct_legal_moves(card, pawn, all_pawns) == []


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
        game = MagicMock(started=True)
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
        assert game.players[PlayerColor.RED].pawns[0].position.square == 4
        assert len(game.players[PlayerColor.RED].hand) == ADULT_HAND

        assert game.players[PlayerColor.YELLOW].color == PlayerColor.YELLOW
        assert game.players[PlayerColor.YELLOW].pawns[0].position.square == 34
        assert len(game.players[PlayerColor.YELLOW].hand) == ADULT_HAND

        assert game.players[PlayerColor.GREEN].color == PlayerColor.GREEN
        assert game.players[PlayerColor.GREEN].pawns[0].position.square == 49
        assert len(game.players[PlayerColor.GREEN].hand) == ADULT_HAND

        assert game.players[PlayerColor.BLUE].color == PlayerColor.BLUE
        assert game.players[PlayerColor.BLUE].pawns[0].position.square == 19
        assert len(game.players[PlayerColor.BLUE].hand) == ADULT_HAND

    def test_construct_legal_moves_no_moves_with_card(self):
        card = MagicMock()

        hand1 = MagicMock()
        hand2 = MagicMock()
        hand = [hand1, hand2]

        pawn1 = MagicMock()
        pawn1.position.home = False
        pawn2 = MagicMock()
        pawn2.position.home = True  # will be filtered out because there are no legal moves for a pawn in home
        pawn3 = MagicMock()
        pawn3.position.home = False
        player_pawns = [pawn1, pawn2, pawn3]

        all_pawns = [MagicMock(), MagicMock()]

        card_pawn1_moves = []
        card_pawn3_moves = []
        legal_moves = [card_pawn1_moves, card_pawn3_moves]
        expected_moves = [Move(card, [])]  # result is a forfeit for the only card

        view = MagicMock()
        view.player = MagicMock(hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls([call(card, pawn1, all_pawns), call(card, pawn3, all_pawns)])

    def test_construct_legal_moves_no_moves_no_card(self):
        card = None

        hand1 = MagicMock()
        hand2 = MagicMock()
        hand = [hand1, hand2]

        pawn1 = MagicMock()
        pawn1.position.home = False
        pawn2 = MagicMock()
        pawn2.position.home = True  # will be filtered out because there are no legal moves for a pawn in home
        pawn3 = MagicMock()
        pawn3.position.home = False
        player_pawns = [pawn1, pawn2, pawn3]

        all_pawns = [MagicMock(), MagicMock()]

        hand1_pawn1_moves = []
        hand1_pawn3_moves = []
        hand2_pawn1_moves = []
        hand2_pawn3_moves = []
        legal_moves = [hand1_pawn1_moves, hand1_pawn3_moves, hand2_pawn1_moves, hand2_pawn3_moves]
        expected_moves = [Move(hand1, []), Move(hand2, [])]  # result is a forfeit for all cards in the hand

        view = MagicMock()
        view.player = MagicMock(hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls(
            [
                call(hand1, pawn1, all_pawns),
                call(hand1, pawn3, all_pawns),
                call(hand2, pawn1, all_pawns),
                call(hand2, pawn3, all_pawns),
            ]
        )

    def test_construct_legal_moves_with_moves_with_card(self):
        card = MagicMock()

        hand1 = MagicMock()
        hand2 = MagicMock()
        hand = [hand1, hand2]

        pawn1 = MagicMock()
        pawn1.position.home = False
        pawn2 = MagicMock()
        pawn2.position.home = True  # will be filtered out because there are no legal moves for a pawn in home
        pawn3 = MagicMock()
        pawn3.position.home = False
        player_pawns = [pawn1, pawn2, pawn3]

        all_pawns = [MagicMock(), MagicMock()]

        card_pawn1_moves = [
            Move(card, [Action(ActionType.MOVE_FROM_START, pawn1)]),
            Move(card, [Action(ActionType.MOVE_FROM_START, pawn1)]),
        ]
        card_pawn3_moves = [Move(card, [Action(ActionType.MOVE_FORWARD, pawn3), Action(ActionType.BUMP_TO_START, pawn3)])]
        legal_moves = [card_pawn1_moves, card_pawn3_moves]
        expected_moves = [
            Move(card, [Action(ActionType.MOVE_FROM_START, pawn1)]),
            Move(card, [Action(ActionType.MOVE_FORWARD, pawn3), Action(ActionType.BUMP_TO_START, pawn3)]),
        ]  # result is a list of all returned moves, with duplicates are removed

        view = MagicMock()
        view.player = MagicMock(hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls([call(card, pawn1, all_pawns), call(card, pawn3, all_pawns)])

    def test_construct_legal_moves_with_moves_no_card(self):
        card = None

        hand1 = MagicMock()
        hand2 = MagicMock()
        hand = [hand1, hand2]

        pawn1 = MagicMock()
        pawn1.position.home = False
        pawn2 = MagicMock()
        pawn2.position.home = True  # will be filtered out because there are no legal moves for a pawn in home
        pawn3 = MagicMock()
        pawn3.position.home = False
        player_pawns = [pawn1, pawn2, pawn3]

        all_pawns = [MagicMock(), MagicMock()]

        hand1_pawn1_moves = [
            Move(hand1, [Action(ActionType.MOVE_FROM_START, pawn1)]),
            Move(hand1, [Action(ActionType.MOVE_FROM_START, pawn1)]),
        ]
        hand1_pawn3_moves = [Move(hand1, [Action(ActionType.MOVE_FORWARD, pawn3), Action(ActionType.BUMP_TO_START, pawn3)])]
        hand2_pawn1_moves = [Move(hand2, [Action(ActionType.CHANGE_PLACES, pawn1)])]
        hand2_pawn3_moves = [Move(hand2, [Action(ActionType.MOVE_BACKARD, pawn3)])]
        legal_moves = [hand1_pawn1_moves, hand1_pawn3_moves, hand2_pawn1_moves, hand2_pawn3_moves]
        expected_moves = [
            Move(hand1, [Action(ActionType.MOVE_FROM_START, pawn1)]),
            Move(hand1, [Action(ActionType.MOVE_FORWARD, pawn3), Action(ActionType.BUMP_TO_START, pawn3)]),
            Move(hand2, [Action(ActionType.CHANGE_PLACES, pawn1)]),
            Move(hand2, [Action(ActionType.MOVE_BACKARD, pawn3)]),
        ]  # result is a list of all returned moves, with duplicates are removed

        view = MagicMock()
        view.player = MagicMock(hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls(
            [
                call(hand1, pawn1, all_pawns),
                call(hand1, pawn3, all_pawns),
                call(hand2, pawn1, all_pawns),
                call(hand2, pawn3, all_pawns),
            ]
        )
