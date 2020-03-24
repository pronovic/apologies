# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access,too-many-locals,too-many-statements

import pytest
from mock import MagicMock, call

from apologies.game import ADULT_HAND, DECK_SIZE, Card, CardType, Game, GameMode, Pawn, PlayerColor, Position
from apologies.rules import Action, ActionType, BoardRules, Move, Rules


class TestAction:
    def test_constructor(self):
        pawn = Pawn(PlayerColor.BLUE, 1, "whatever")
        position = Position().move_to_square(32)
        action = Action(ActionType.MOVE_TO_START, pawn, position)
        assert action.actiontype == ActionType.MOVE_TO_START
        assert action.pawn is pawn
        assert action.position is position


class TestMove:
    def test_constructor(self):
        card = Card(3, CardType.CARD_12)
        actions = [Action(ActionType.MOVE_TO_START, pawn=Pawn(PlayerColor.BLUE, 1, "whatever"))]
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
        pawn2 = MagicMock()
        player_pawns = [pawn1, pawn2]

        all_pawns = [MagicMock(), MagicMock()]

        card_pawn1_moves = []
        card_pawn2_moves = []
        legal_moves = [card_pawn1_moves, card_pawn2_moves]
        expected_moves = [Move(card, [])]  # result is a forfeit for the only card

        view = MagicMock()
        view.player = MagicMock(color=PlayerColor.RED, hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls(
            [call(PlayerColor.RED, card, pawn1, all_pawns), call(PlayerColor.RED, card, pawn2, all_pawns)]
        )

    def test_construct_legal_moves_no_moves_no_card(self):
        card = None

        hand1 = MagicMock()
        hand2 = MagicMock()
        hand = [hand1, hand2]

        pawn1 = MagicMock()
        pawn2 = MagicMock()
        player_pawns = [pawn1, pawn2]

        all_pawns = [MagicMock(), MagicMock()]

        hand1_pawn1_moves = []
        hand1_pawn2_moves = []
        hand2_pawn1_moves = []
        hand2_pawn2_moves = []
        legal_moves = [hand1_pawn1_moves, hand1_pawn2_moves, hand2_pawn1_moves, hand2_pawn2_moves]
        expected_moves = [Move(hand1, []), Move(hand2, [])]  # result is a forfeit for all cards in the hand

        view = MagicMock()
        view.player = MagicMock(color=PlayerColor.RED, hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls(
            [
                call(PlayerColor.RED, hand1, pawn1, all_pawns),
                call(PlayerColor.RED, hand1, pawn2, all_pawns),
                call(PlayerColor.RED, hand2, pawn1, all_pawns),
                call(PlayerColor.RED, hand2, pawn2, all_pawns),
            ]
        )

    def test_construct_legal_moves_with_moves_with_card(self):
        card = MagicMock()

        hand1 = MagicMock()
        hand2 = MagicMock()
        hand = [hand1, hand2]

        pawn1 = MagicMock()
        pawn2 = MagicMock()
        player_pawns = [pawn1, pawn2]

        all_pawns = [MagicMock(), MagicMock()]

        card_pawn1_moves = [
            Move(card, [Action(ActionType.MOVE_TO_START, pawn1)]),
            Move(card, [Action(ActionType.MOVE_TO_START, pawn1)]),
        ]
        card_pawn2_moves = [Move(card, [Action(ActionType.MOVE_TO_POSITION, pawn2), Action(ActionType.MOVE_TO_START, pawn2)])]
        legal_moves = [card_pawn1_moves, card_pawn2_moves]
        expected_moves = [
            Move(card, [Action(ActionType.MOVE_TO_START, pawn1)]),
            Move(card, [Action(ActionType.MOVE_TO_POSITION, pawn2), Action(ActionType.MOVE_TO_START, pawn2)]),
        ]  # result is a list of all returned moves, with duplicates are removed

        view = MagicMock()
        view.player = MagicMock(color=PlayerColor.RED, hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls(
            [call(PlayerColor.RED, card, pawn1, all_pawns), call(PlayerColor.RED, card, pawn2, all_pawns)]
        )

    def test_construct_legal_moves_with_moves_no_card(self):
        card = None

        hand1 = MagicMock()
        hand2 = MagicMock()
        hand = [hand1, hand2]

        pawn1 = MagicMock()
        pawn2 = MagicMock()
        player_pawns = [pawn1, pawn2]

        all_pawns = [MagicMock(), MagicMock()]

        hand1_pawn1_moves = [
            Move(hand1, [Action(ActionType.MOVE_TO_START, pawn1)]),
            Move(hand1, [Action(ActionType.MOVE_TO_START, pawn1)]),
        ]
        hand1_pawn2_moves = [Move(hand1, [Action(ActionType.MOVE_TO_START, pawn2), Action(ActionType.MOVE_TO_POSITION, pawn2)])]
        hand2_pawn1_moves = [Move(hand2, [Action(ActionType.MOVE_TO_POSITION, pawn1, Position())])]
        hand2_pawn2_moves = [Move(hand2, [Action(ActionType.MOVE_TO_POSITION, pawn2, Position())])]
        legal_moves = [hand1_pawn1_moves, hand1_pawn2_moves, hand2_pawn1_moves, hand2_pawn2_moves]
        expected_moves = [
            Move(hand1, [Action(ActionType.MOVE_TO_START, pawn1)]),
            Move(hand1, [Action(ActionType.MOVE_TO_START, pawn2), Action(ActionType.MOVE_TO_POSITION, pawn2)]),
            Move(hand2, [Action(ActionType.MOVE_TO_POSITION, pawn1, Position())]),
            Move(hand2, [Action(ActionType.MOVE_TO_POSITION, pawn2, Position())]),
        ]  # result is a list of all returned moves, with duplicates are removed

        view = MagicMock()
        view.player = MagicMock(color=PlayerColor.RED, hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls(
            [
                call(PlayerColor.RED, hand1, pawn1, all_pawns),
                call(PlayerColor.RED, hand1, pawn2, all_pawns),
                call(PlayerColor.RED, hand2, pawn1, all_pawns),
                call(PlayerColor.RED, hand2, pawn2, all_pawns),
            ]
        )


class TestBoardRules:
    def test_constructor(self):
        BoardRules()  # just make sure it doesn't blow up

    def test_calculate_position_home(self):
        for color in PlayerColor:
            with pytest.raises(ValueError):
                BoardRules().position(color, Position().move_to_home(), 1)

    def test_calculate_position_start(self):
        for color in PlayerColor:
            with pytest.raises(ValueError):
                BoardRules().position(color, Position().move_to_home(), 1)

    def test_calculate_position_from_safe(self):
        for color in PlayerColor:
            assert BoardRules().position(color, Position().move_to_safe(0), 0) == Position().move_to_safe(0)
            assert BoardRules().position(color, Position().move_to_safe(3), 0) == Position().move_to_safe(3)

        for color in PlayerColor:
            assert BoardRules().position(color, Position().move_to_safe(0), 1) == Position().move_to_safe(1)
            assert BoardRules().position(color, Position().move_to_safe(2), 2) == Position().move_to_safe(4)
            assert BoardRules().position(color, Position().move_to_safe(4), 1) == Position().move_to_home()

        for color in PlayerColor:
            with pytest.raises(ValueError):
                BoardRules().position(color, Position().move_to_safe(3), 3)
                BoardRules().position(color, Position().move_to_safe(4), 2)

        for color in PlayerColor:
            assert BoardRules().position(color, Position().move_to_safe(4), -2) == Position().move_to_safe(2)
            assert BoardRules().position(color, Position().move_to_safe(1), -1) == Position().move_to_safe(0)

        assert BoardRules().position(PlayerColor.RED, Position().move_to_safe(0), -1) == Position().move_to_square(2)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_safe(0), -2) == Position().move_to_square(1)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_safe(0), -3) == Position().move_to_square(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_safe(0), -4) == Position().move_to_square(59)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_safe(0), -5) == Position().move_to_square(58)

        assert BoardRules().position(PlayerColor.BLUE, Position().move_to_safe(0), -1) == Position().move_to_square(17)
        assert BoardRules().position(PlayerColor.BLUE, Position().move_to_safe(0), -2) == Position().move_to_square(16)

        assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_safe(0), -1) == Position().move_to_square(32)
        assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_safe(0), -2) == Position().move_to_square(31)

        assert BoardRules().position(PlayerColor.GREEN, Position().move_to_safe(0), -1) == Position().move_to_square(47)
        assert BoardRules().position(PlayerColor.GREEN, Position().move_to_safe(0), -2) == Position().move_to_square(46)

    def test_calculate_position_from_square(self):
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(58), 1) == Position().move_to_square(59)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(59), 1) == Position().move_to_square(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(54), 5) == Position().move_to_square(59)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(54), 6) == Position().move_to_square(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(54), 7) == Position().move_to_square(1)

        for color in PlayerColor:
            assert BoardRules().position(color, Position().move_to_square(54), 5) == Position().move_to_square(59)
            assert BoardRules().position(color, Position().move_to_square(54), 6) == Position().move_to_square(0)
            assert BoardRules().position(color, Position().move_to_square(54), 7) == Position().move_to_square(1)
            assert BoardRules().position(color, Position().move_to_square(58), 1) == Position().move_to_square(59)
            assert BoardRules().position(color, Position().move_to_square(59), 1) == Position().move_to_square(0)
            assert BoardRules().position(color, Position().move_to_square(0), 1) == Position().move_to_square(1)
            assert BoardRules().position(color, Position().move_to_square(1), 1) == Position().move_to_square(2)
            assert BoardRules().position(color, Position().move_to_square(10), 5) == Position().move_to_square(15)

        for color in PlayerColor:
            assert BoardRules().position(color, Position().move_to_square(59), -5) == Position().move_to_square(54)
            assert BoardRules().position(color, Position().move_to_square(0), -6) == Position().move_to_square(54)
            assert BoardRules().position(color, Position().move_to_square(1), -7) == Position().move_to_square(54)
            assert BoardRules().position(color, Position().move_to_square(59), -1) == Position().move_to_square(58)
            assert BoardRules().position(color, Position().move_to_square(0), -1) == Position().move_to_square(59)
            assert BoardRules().position(color, Position().move_to_square(1), -1) == Position().move_to_square(0)
            assert BoardRules().position(color, Position().move_to_square(2), -1) == Position().move_to_square(1)
            assert BoardRules().position(color, Position().move_to_square(15), -5) == Position().move_to_square(10)

        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(0), 3) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(1), 2) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(2), 1) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(1), 3) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(2), 2) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(2), 6) == Position().move_to_home()
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(51), 12) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(52), 12) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(58), 5) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.RED, Position().move_to_square(59), 4) == Position().move_to_safe(0)

        with pytest.raises(ValueError):
            assert BoardRules().position(PlayerColor.RED, Position().move_to_square(2), 7) == Position().move_to_home()

        assert BoardRules().position(PlayerColor.BLUE, Position().move_to_square(16), 2) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.BLUE, Position().move_to_square(17), 1) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.BLUE, Position().move_to_square(16), 3) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.BLUE, Position().move_to_square(17), 2) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.BLUE, Position().move_to_square(17), 6) == Position().move_to_home()
        with pytest.raises(ValueError):
            assert BoardRules().position(PlayerColor.BLUE, Position().move_to_square(17), 7) == Position().move_to_home()

        assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_square(31), 2) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_square(32), 1) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_square(31), 3) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_square(32), 2) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_square(32), 6) == Position().move_to_home()
        with pytest.raises(ValueError):
            assert BoardRules().position(PlayerColor.YELLOW, Position().move_to_square(32), 7) == Position().move_to_home()

        assert BoardRules().position(PlayerColor.GREEN, Position().move_to_square(46), 2) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.GREEN, Position().move_to_square(47), 1) == Position().move_to_safe(0)
        assert BoardRules().position(PlayerColor.GREEN, Position().move_to_square(46), 3) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.GREEN, Position().move_to_square(47), 2) == Position().move_to_safe(1)
        assert BoardRules().position(PlayerColor.GREEN, Position().move_to_square(47), 6) == Position().move_to_home()
        with pytest.raises(ValueError):
            assert BoardRules().position(PlayerColor.GREEN, Position().move_to_square(47), 7) == Position().move_to_home()
