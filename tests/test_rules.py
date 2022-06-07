# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access,too-many-locals,too-many-statements,assigning-non-slot

from unittest.mock import MagicMock, call, patch

import pytest

from apologies.game import ADULT_HAND, DECK_SIZE, PAWNS, Card, CardType, Game, GameMode, Pawn, PlayerColor, Position
from apologies.rules import Action, ActionType, BoardRules, Move, Rules

_UUID = MagicMock(return_value=MagicMock(hex="uuid"))  # any call to get a random UUID returns a UUID with hex value "uuid"


class TestAction:
    def test_constructor(self):
        pawn = Pawn(PlayerColor.BLUE, 1, "whatever")
        position = Position().move_to_square(32)
        action = Action(ActionType.MOVE_TO_START, pawn, position)
        assert action.actiontype == ActionType.MOVE_TO_START
        assert action.pawn is pawn
        assert action.position is position


class TestMove:
    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_constructor_uuid(self):
        card = Card(3, CardType.CARD_12)
        actions = [Action(ActionType.MOVE_TO_START, pawn=Pawn(PlayerColor.BLUE, 1, "whatever"))]
        move = Move(card, actions)
        assert move.card is card
        assert move.actions == actions
        assert move.id == "uuid"

    def test_constructor_uuid_unique(self):
        card = Card(3, CardType.CARD_12)
        actions = [Action(ActionType.MOVE_TO_START, pawn=Pawn(PlayerColor.BLUE, 1, "whatever"))]
        move1 = Move(card, actions)
        move2 = Move(card, actions)
        assert move1.id != move2.id  # just make sure we get a unique UUID each time in the default case

    def test_constructor_explicit(self):
        card = Card(3, CardType.CARD_12)
        actions = [Action(ActionType.MOVE_TO_START, pawn=Pawn(PlayerColor.BLUE, 1, "whatever"))]
        move = Move(card, actions, id="whatever")
        assert move.card is card
        assert move.actions == actions
        assert move.id == "whatever"


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

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
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

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
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

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
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
        ]  # result is a list of all returned moves, with duplicates removed

        view = MagicMock()
        view.player = MagicMock(color=PlayerColor.RED, hand=hand, pawns=player_pawns)
        view.all_pawns = MagicMock(return_value=all_pawns)

        rules = Rules(GameMode.STANDARD)
        rules._board_rules.construct_legal_moves = MagicMock(side_effect=legal_moves)
        assert rules.construct_legal_moves(view, card=card) == expected_moves

        rules._board_rules.construct_legal_moves.assert_has_calls(
            [call(PlayerColor.RED, card, pawn1, all_pawns), call(PlayerColor.RED, card, pawn2, all_pawns)]
        )

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
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
        ]  # result is a list of all returned moves, with duplicates removed

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

    def test_execute_move(self):
        rules = Rules(GameMode.STANDARD)
        game = Game(4)
        player = game.players[PlayerColor.RED]

        for color in PlayerColor:
            for pawn in range(PAWNS):
                game.players[color].pawns[pawn].position.move_to_start = MagicMock()
                game.players[color].pawns[pawn].position.move_to_position = MagicMock()

        move = Move(
            MagicMock(),
            actions=[
                Action(ActionType.MOVE_TO_POSITION, MagicMock(color=PlayerColor.RED, index=1), Position().move_to_square(10)),
                Action(ActionType.MOVE_TO_POSITION, MagicMock(color=PlayerColor.YELLOW, index=3), Position().move_to_square(11)),
            ],
            side_effects=[
                Action(ActionType.MOVE_TO_START, MagicMock(color=PlayerColor.BLUE, index=2)),
                Action(ActionType.MOVE_TO_POSITION, MagicMock(color=PlayerColor.GREEN, index=0), Position().move_to_square(12)),
            ],
        )

        rules.execute_move(game, player, move)

        game.players[PlayerColor.RED].pawns[1].position.move_to_position.assert_called_once_with(Position().move_to_square(10))
        game.players[PlayerColor.YELLOW].pawns[3].position.move_to_position.assert_called_once_with(Position().move_to_square(11))
        game.players[PlayerColor.BLUE].pawns[2].position.move_to_start.assert_called_once()
        game.players[PlayerColor.GREEN].pawns[0].position.move_to_position.assert_called_once_with(Position().move_to_square(12))

    def test_evaluate_move(self):
        move = Move(
            MagicMock(),
            actions=[
                Action(ActionType.MOVE_TO_POSITION, MagicMock(color=PlayerColor.RED, index=1), Position().move_to_square(10)),
                Action(ActionType.MOVE_TO_POSITION, MagicMock(color=PlayerColor.YELLOW, index=3), Position().move_to_square(11)),
            ],
            side_effects=[
                Action(ActionType.MOVE_TO_START, MagicMock(color=PlayerColor.BLUE, index=2)),
                Action(ActionType.MOVE_TO_POSITION, MagicMock(color=PlayerColor.GREEN, index=0), Position().move_to_square(12)),
            ],
        )

        game = Game(4)
        view = game.create_player_view(PlayerColor.RED)

        expected = view.copy()
        expected.player.pawns[1].position.move_to_square(10)
        expected.opponents[PlayerColor.YELLOW].pawns[3].position.move_to_square(11)
        expected.opponents[PlayerColor.BLUE].pawns[2].position.move_to_start()
        expected.opponents[PlayerColor.GREEN].pawns[0].position.move_to_square(12)

        assert expected == Rules.evaluate_move(view, move)


RED = PlayerColor.RED
YELLOW = PlayerColor.YELLOW
GREEN = PlayerColor.GREEN
BLUE = PlayerColor.BLUE


def _pawn(color, start=False, home=False, safe=None, square=None):
    position = Position(start=start, home=home, safe=safe, square=square)
    return Pawn(color, 0, "name", position)


class TestPosition:
    def test_constructor(self):
        BoardRules()  # just make sure it doesn't blow up

    def test_distance_to_home(self):
        # distance from home is always 0
        for color in [RED, YELLOW, GREEN, BLUE]:
            assert BoardRules.distance_to_home(_pawn(color, home=True)) == 0

        # distance from start is always 65
        for color in [RED, YELLOW, GREEN, BLUE]:
            assert BoardRules.distance_to_home(_pawn(color, start=True)) == 65

        # distance from within safe is always <= 5
        assert BoardRules.distance_to_home(_pawn(RED, safe=0)) == 5
        assert BoardRules.distance_to_home(_pawn(BLUE, safe=1)) == 4
        assert BoardRules.distance_to_home(_pawn(YELLOW, safe=2)) == 3
        assert BoardRules.distance_to_home(_pawn(GREEN, safe=3)) == 2
        assert BoardRules.distance_to_home(_pawn(GREEN, safe=4)) == 1

        # distance from circle is always 64
        assert BoardRules.distance_to_home(_pawn(RED, square=4)) == 64
        assert BoardRules.distance_to_home(_pawn(BLUE, square=19)) == 64
        assert BoardRules.distance_to_home(_pawn(YELLOW, square=34)) == 64
        assert BoardRules.distance_to_home(_pawn(GREEN, square=49)) == 64

        # distance from square between turn and circle is always 65
        assert BoardRules.distance_to_home(_pawn(RED, square=3)) == 65
        assert BoardRules.distance_to_home(_pawn(BLUE, square=18)) == 65
        assert BoardRules.distance_to_home(_pawn(YELLOW, square=33)) == 65
        assert BoardRules.distance_to_home(_pawn(GREEN, square=48)) == 65

        # distance from turn is always 6
        assert BoardRules.distance_to_home(_pawn(RED, square=2)) == 6
        assert BoardRules.distance_to_home(_pawn(BLUE, square=17)) == 6
        assert BoardRules.distance_to_home(_pawn(YELLOW, square=32)) == 6
        assert BoardRules.distance_to_home(_pawn(GREEN, square=47)) == 6

        # check some arbitrary squares
        assert BoardRules.distance_to_home(_pawn(RED, square=1)) == 7
        assert BoardRules.distance_to_home(_pawn(RED, square=0)) == 8
        assert BoardRules.distance_to_home(_pawn(RED, square=59)) == 9
        assert BoardRules.distance_to_home(_pawn(RED, square=9)) == 59
        assert BoardRules.distance_to_home(_pawn(BLUE, square=0)) == 23
        assert BoardRules.distance_to_home(_pawn(GREEN, square=40)) == 13

    def test_calculate_position_home(self):
        for color in PlayerColor:
            with pytest.raises(ValueError):
                BoardRules()._position(color, Position().move_to_home(), 1)

    def test_calculate_position_start(self):
        for color in PlayerColor:
            with pytest.raises(ValueError):
                BoardRules()._position(color, Position().move_to_home(), 1)

    def test_calculate_position_from_safe(self):
        for color in PlayerColor:
            assert BoardRules()._position(color, Position().move_to_safe(0), 0) == Position().move_to_safe(0)
            assert BoardRules()._position(color, Position().move_to_safe(3), 0) == Position().move_to_safe(3)

        for color in PlayerColor:
            assert BoardRules()._position(color, Position().move_to_safe(0), 1) == Position().move_to_safe(1)
            assert BoardRules()._position(color, Position().move_to_safe(2), 2) == Position().move_to_safe(4)
            assert BoardRules()._position(color, Position().move_to_safe(4), 1) == Position().move_to_home()

        for color in PlayerColor:
            with pytest.raises(ValueError):
                BoardRules()._position(color, Position().move_to_safe(3), 3)
                BoardRules()._position(color, Position().move_to_safe(4), 2)

        for color in PlayerColor:
            assert BoardRules()._position(color, Position().move_to_safe(4), -2) == Position().move_to_safe(2)
            assert BoardRules()._position(color, Position().move_to_safe(1), -1) == Position().move_to_safe(0)

        assert BoardRules()._position(PlayerColor.RED, Position().move_to_safe(0), -1) == Position().move_to_square(2)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_safe(0), -2) == Position().move_to_square(1)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_safe(0), -3) == Position().move_to_square(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_safe(0), -4) == Position().move_to_square(59)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_safe(0), -5) == Position().move_to_square(58)

        assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_safe(0), -1) == Position().move_to_square(17)
        assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_safe(0), -2) == Position().move_to_square(16)

        assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_safe(0), -1) == Position().move_to_square(32)
        assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_safe(0), -2) == Position().move_to_square(31)

        assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_safe(0), -1) == Position().move_to_square(47)
        assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_safe(0), -2) == Position().move_to_square(46)

    def test_calculate_position_from_square(self):
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(58), 1) == Position().move_to_square(59)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(59), 1) == Position().move_to_square(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(54), 5) == Position().move_to_square(59)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(54), 6) == Position().move_to_square(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(54), 7) == Position().move_to_square(1)

        for color in PlayerColor:
            assert BoardRules()._position(color, Position().move_to_square(54), 5) == Position().move_to_square(59)
            assert BoardRules()._position(color, Position().move_to_square(54), 6) == Position().move_to_square(0)
            assert BoardRules()._position(color, Position().move_to_square(54), 7) == Position().move_to_square(1)
            assert BoardRules()._position(color, Position().move_to_square(58), 1) == Position().move_to_square(59)
            assert BoardRules()._position(color, Position().move_to_square(59), 1) == Position().move_to_square(0)
            assert BoardRules()._position(color, Position().move_to_square(0), 1) == Position().move_to_square(1)
            assert BoardRules()._position(color, Position().move_to_square(1), 1) == Position().move_to_square(2)
            assert BoardRules()._position(color, Position().move_to_square(10), 5) == Position().move_to_square(15)

        for color in PlayerColor:
            assert BoardRules()._position(color, Position().move_to_square(59), -5) == Position().move_to_square(54)
            assert BoardRules()._position(color, Position().move_to_square(0), -6) == Position().move_to_square(54)
            assert BoardRules()._position(color, Position().move_to_square(1), -7) == Position().move_to_square(54)
            assert BoardRules()._position(color, Position().move_to_square(59), -1) == Position().move_to_square(58)
            assert BoardRules()._position(color, Position().move_to_square(0), -1) == Position().move_to_square(59)
            assert BoardRules()._position(color, Position().move_to_square(1), -1) == Position().move_to_square(0)
            assert BoardRules()._position(color, Position().move_to_square(2), -1) == Position().move_to_square(1)
            assert BoardRules()._position(color, Position().move_to_square(15), -5) == Position().move_to_square(10)

        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(0), 3) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(1), 2) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(2), 1) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(1), 3) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(2), 2) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(2), 6) == Position().move_to_home()
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(51), 12) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(52), 12) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(58), 5) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(59), 4) == Position().move_to_safe(0)

        with pytest.raises(ValueError):
            assert BoardRules()._position(PlayerColor.RED, Position().move_to_square(2), 7) == Position().move_to_home()

        assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_square(16), 2) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_square(17), 1) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_square(16), 3) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_square(17), 2) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_square(17), 6) == Position().move_to_home()
        with pytest.raises(ValueError):
            assert BoardRules()._position(PlayerColor.BLUE, Position().move_to_square(17), 7) == Position().move_to_home()

        assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_square(31), 2) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_square(32), 1) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_square(31), 3) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_square(32), 2) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_square(32), 6) == Position().move_to_home()
        with pytest.raises(ValueError):
            assert BoardRules()._position(PlayerColor.YELLOW, Position().move_to_square(32), 7) == Position().move_to_home()

        assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_square(46), 2) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_square(47), 1) == Position().move_to_safe(0)
        assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_square(46), 3) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_square(47), 2) == Position().move_to_safe(1)
        assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_square(47), 6) == Position().move_to_home()
        with pytest.raises(ValueError):
            assert BoardRules()._position(PlayerColor.GREEN, Position().move_to_square(47), 7) == Position().move_to_home()


def _setup_game():
    game = Game(4)
    for color in PlayerColor:
        for pawn in range(PAWNS):
            game.players[color].pawns[pawn].position.move_to_home()
    return game


def _square(pawn, square):
    return Action(ActionType.MOVE_TO_POSITION, pawn, Position().move_to_square(square))


def _safe(pawn, square):
    return Action(ActionType.MOVE_TO_POSITION, pawn, Position().move_to_safe(square))


def _start(pawn):
    return Action(ActionType.MOVE_TO_START, pawn)


def _bump(view, color, index):
    if view.player.color == color:
        return _start(view.player.pawns[index])
    return _start(view.opponents[color].pawns[index])


def _swap(view, pawn, color, index):
    other = view.opponents[color].pawns[index]
    return [_square(pawn, other.position.square), _square(other, pawn.position.square)]


def _home(pawn):
    return Action(ActionType.MOVE_TO_POSITION, pawn, Position().move_to_home())


def _legal_moves(color, game, index, cardtype):
    card = Card(id="test", cardtype=CardType(cardtype))
    view = game.create_player_view(color)
    pawn = view.player.pawns[index]
    rules = BoardRules()
    moves = rules.construct_legal_moves(view.player.color, card, pawn, view.all_pawns())
    return card, pawn, view, moves


class TestLegalMoves:
    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_1(self):
        # No legal moves if no pawn in start, on the board, or in safe
        game = _setup_game()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == []

        # Move pawn from start with no conflicts
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_start()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_square(pawn, 4)], side_effects=[])]

        # Move pawn from start with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_start()
        game.players[RED].pawns[1].position.move_to_square(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == []  # can't start because we have a pawn there already

        # Move pawn from start with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_start()
        game.players[YELLOW].pawns[0].position.move_to_square(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_square(pawn, 4)], side_effects=[_bump(view, YELLOW, 0)])]

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_square(pawn, 7)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(7)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[GREEN].pawns[1].position.move_to_square(7)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_square(pawn, 7)], side_effects=[_bump(view, GREEN, 1)])]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_2(self):
        # No legal moves if no pawn in start, on the board, or in safe
        game = _setup_game()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == []

        # Move pawn from start with no conflicts
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_start()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "2")
        assert moves == [Move(card, actions=[_square(pawn, 4)], side_effects=[])]

        # Move pawn from start with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_start()
        game.players[RED].pawns[1].position.move_to_square(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "2")
        assert moves == []  # can't start because we have a pawn there already

        # Move pawn from start with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_start()
        game.players[YELLOW].pawns[0].position.move_to_square(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "2")
        assert moves == [Move(card, actions=[_square(pawn, 4)], side_effects=[_bump(view, YELLOW, 0)])]

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "2")
        assert moves == [Move(card, actions=[_square(pawn, 8)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(8)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "2")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[GREEN].pawns[1].position.move_to_square(8)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "2")
        assert moves == [Move(card, actions=[_square(pawn, 8)], side_effects=[_bump(view, GREEN, 1)])]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_3(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "3")
        assert moves == []

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "3")
        assert moves == [Move(card, actions=[_square(pawn, 9)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(9)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "3")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[GREEN].pawns[1].position.move_to_square(9)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "3")
        assert moves == [Move(card, actions=[_square(pawn, 9)], side_effects=[_bump(view, GREEN, 1)])]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_4(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "4")
        assert moves == []

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "4")
        assert moves == [Move(card, actions=[_square(pawn, 2)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(2)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "4")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[GREEN].pawns[1].position.move_to_square(2)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "4")
        assert moves == [Move(card, actions=[_square(pawn, 2)], side_effects=[_bump(view, GREEN, 1)])]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_5(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "5")
        assert moves == []

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "5")
        assert moves == [Move(card, actions=[_square(pawn, 11)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(11)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "5")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[GREEN].pawns[1].position.move_to_square(11)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "5")
        assert moves == [Move(card, actions=[_square(pawn, 11)], side_effects=[_bump(view, GREEN, 1)])]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_7(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "7")
        assert moves == []

        # One move available if there is one pawn on the board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "7")
        assert moves == [Move(card, actions=[_square(pawn, 13)], side_effects=[])]

        # Multiple moves available if there is more than one pawn on the board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[2].position.move_to_square(55)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "7")
        other = view.player.pawns[2]
        assert moves == [
            Move(card, actions=[_square(pawn, 13)], side_effects=[]),  # move our pawn 7
            Move(card, actions=[_square(pawn, 7), _square(other, 1)], side_effects=[]),  # split (1, 6)
            Move(card, actions=[_square(pawn, 8), _square(other, 0)], side_effects=[]),  # split (2, 5)
            Move(card, actions=[_square(pawn, 9), _square(other, 59)], side_effects=[]),  # split (3, 4)
            Move(card, actions=[_square(pawn, 10), _square(other, 58)], side_effects=[]),  # split (4, 3)
            Move(card, actions=[_square(pawn, 11), _square(other, 57)], side_effects=[]),  # split (5, 2)
            Move(card, actions=[_square(pawn, 12), _square(other, 56)], side_effects=[]),  # split (6, 1)
        ]

        # Either half of a move might bump an opponent back to start
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[2].position.move_to_square(55)
        game.players[GREEN].pawns[1].position.move_to_square(10)
        game.players[BLUE].pawns[3].position.move_to_square(56)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "7")
        other = view.player.pawns[2]
        assert moves == [
            Move(card, actions=[_square(pawn, 13)], side_effects=[]),  # move our pawn 7
            Move(card, actions=[_square(pawn, 7), _square(other, 1)], side_effects=[]),  # split (1, 6)
            Move(card, actions=[_square(pawn, 8), _square(other, 0)], side_effects=[]),  # split (2, 5)
            Move(card, actions=[_square(pawn, 9), _square(other, 59)], side_effects=[]),  # split (3, 4)
            Move(card, actions=[_square(pawn, 10), _square(other, 58)], side_effects=[_bump(view, GREEN, 1)]),  # split (4, 3)
            Move(card, actions=[_square(pawn, 11), _square(other, 57)], side_effects=[]),  # split (5, 2)
            Move(card, actions=[_square(pawn, 12), _square(other, 56)], side_effects=[_bump(view, BLUE, 3)]),  # split (6, 1)
        ]

        # If either half of the move has a conflict with another pawn of the same color, the entire move is invalidated
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(9)
        game.players[RED].pawns[2].position.move_to_square(55)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "7")
        other1 = view.player.pawns[1]
        other2 = view.player.pawns[2]
        assert moves == [
            Move(card, actions=[_square(pawn, 13)], side_effects=[]),  # move our pawn 7
            Move(card, actions=[_square(pawn, 7), _square(other1, 15)], side_effects=[]),  # split (1, 6)
            Move(card, actions=[_square(pawn, 8), _square(other1, 14)], side_effects=[]),  # split (2, 5)
            Move(card, actions=[_square(pawn, 9), _square(other1, 13)], side_effects=[]),  # split (3, 4)
            Move(card, actions=[_square(pawn, 10), _square(other1, 12)], side_effects=[]),  # split (4, 3)
            Move(card, actions=[_square(pawn, 11), _square(other1, 11)], side_effects=[]),  # split (5, 2)
            Move(card, actions=[_square(pawn, 12), _square(other1, 10)], side_effects=[]),  # split (6, 1)
            Move(card, actions=[_square(pawn, 7), _square(other2, 1)], side_effects=[]),  # split (1, 6)
            Move(card, actions=[_square(pawn, 8), _square(other2, 0)], side_effects=[]),  # split (2, 5)
            # the move for square 9 is disallowed because pawn[1] already lives there, and isn't part of this action
            Move(card, actions=[_square(pawn, 10), _square(other2, 58)], side_effects=[]),  # split (4, 3)
            Move(card, actions=[_square(pawn, 11), _square(other2, 57)], side_effects=[]),  # split (5, 2)
            Move(card, actions=[_square(pawn, 12), _square(other2, 56)], side_effects=[]),  # split (6, 1)
        ]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_8(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "8")
        assert moves == []

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "8")
        assert moves == [Move(card, actions=[_square(pawn, 14)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(14)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "8")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[GREEN].pawns[1].position.move_to_square(14)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "8")
        assert moves == [Move(card, actions=[_square(pawn, 14)], side_effects=[_bump(view, GREEN, 1)])]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_10(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "10")
        assert moves == []

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(5)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "10")
        assert moves == [
            Move(card, actions=[_square(pawn, 15)], side_effects=[]),
            Move(card, actions=[_square(pawn, 4)], side_effects=[]),
        ]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(5)
        game.players[RED].pawns[1].position.move_to_square(15)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "10")
        assert moves == [Move(card, actions=[_square(pawn, 4)], side_effects=[])]  # can't move because we have a pawn there already

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(5)
        game.players[RED].pawns[1].position.move_to_square(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "10")
        assert moves == [
            Move(card, actions=[_square(pawn, 15)], side_effects=[])
        ]  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(5)
        game.players[GREEN].pawns[1].position.move_to_square(15)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "10")
        assert moves == [
            Move(card, actions=[_square(pawn, 15)], side_effects=[_bump(view, GREEN, 1)]),
            Move(card, actions=[_square(pawn, 4)], side_effects=[]),
        ]

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(5)
        game.players[GREEN].pawns[1].position.move_to_square(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "10")
        assert moves == [
            Move(card, actions=[_square(pawn, 15)], side_effects=[]),
            Move(card, actions=[_square(pawn, 4)], side_effects=[_bump(view, GREEN, 1)]),
        ]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_11(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "11")
        assert moves == []

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(15)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "11")
        assert moves == [Move(card, actions=[_square(pawn, 26)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(15)
        game.players[RED].pawns[1].position.move_to_square(26)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "11")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color), which also gets us a swap opportunity
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(15)
        game.players[GREEN].pawns[1].position.move_to_square(26)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "11")
        assert moves == [
            Move(card, actions=_swap(view, pawn, GREEN, 1), side_effects=[]),
            Move(card, actions=[_square(pawn, 26)], side_effects=[_bump(view, GREEN, 1)]),
        ]

        # Swap pawns elsewhere on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(15)
        game.players[RED].pawns[1].position.move_to_square(32)  # can't be swapped, same color
        game.players[GREEN].pawns[0].position.move_to_start()  # can't be swapped, in start area
        game.players[YELLOW].pawns[0].position.move_to_safe(0)  # can't be swapped, in safe area
        game.players[YELLOW].pawns[3].position.move_to_square(52)  # can be swapped, on board
        game.players[BLUE].pawns[1].position.move_to_square(19)  # can be swapped, on board\
        card, pawn, view, moves = _legal_moves(RED, game, 0, "11")
        assert moves == [
            Move(card, actions=_swap(view, pawn, YELLOW, 3), side_effects=[]),
            Move(card, actions=_swap(view, pawn, BLUE, 1), side_effects=[]),
            Move(card, actions=[_square(pawn, 26)], side_effects=[]),
        ]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_12(self):
        # No legal moves if no pawn on the board, or in safe
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_home()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "12")
        assert moves == []

        # Move pawn on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "12")
        assert moves == [Move(card, actions=[_square(pawn, 18)], side_effects=[])]

        # Move pawn on board with conflict (same color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[RED].pawns[1].position.move_to_square(18)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "12")
        assert moves == []  # can't move because we have a pawn there already

        # Move pawn on board with conflict (different color)
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(6)
        game.players[GREEN].pawns[1].position.move_to_square(18)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "12")
        assert moves == [Move(card, actions=[_square(pawn, 18)], side_effects=[_bump(view, GREEN, 1)])]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_card_apologies(self):
        # No legal moves if no pawn in start
        game = _setup_game()
        card, pawn, view, moves = _legal_moves(RED, game, 0, "A")
        game.players[YELLOW].pawns[3].position.move_to_square(52)  # can be swapped, on board
        game.players[BLUE].pawns[1].position.move_to_square(19)  # can be swapped, on board
        assert moves == []

        # Swap pawns elsewhere on board
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_start()
        game.players[GREEN].pawns[0].position.move_to_start()  # can't be swapped, in start area
        game.players[YELLOW].pawns[0].position.move_to_safe(0)  # can't be swapped, in safe area
        game.players[YELLOW].pawns[3].position.move_to_square(52)  # can be swapped, on board
        game.players[BLUE].pawns[1].position.move_to_square(19)  # can be swapped, on board
        card, pawn, view, moves = _legal_moves(RED, game, 0, "A")
        assert moves == [
            Move(card, actions=[_square(pawn, 52), _bump(view, YELLOW, 3)], side_effects=[]),
            Move(card, actions=[_square(pawn, 19), _bump(view, BLUE, 1)], side_effects=[]),
        ]

    @patch("apologies.rules.uuid.uuid4", new=_UUID)
    def test_construct_legal_moves_special(self):
        # Move pawn into safe zone
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(2)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_safe(pawn, 0)], side_effects=[])]

        # Move pawn to home
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_safe(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_home(pawn)], side_effects=[])]

        # Move pawn past home
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_safe(4)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "2")
        assert moves == []  # No moves, because it isn't legal

        # Slide of the same color
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(8)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_square(pawn, 9)], side_effects=[])]

        # Slide of a different color
        game = _setup_game()
        game.players[RED].pawns[0].position.move_to_square(15)
        game.players[RED].pawns[1].position.move_to_square(17)
        game.players[YELLOW].pawns[2].position.move_to_square(18)
        card, pawn, view, moves = _legal_moves(RED, game, 0, "1")
        assert moves == [Move(card, actions=[_square(pawn, 19)], side_effects=[_bump(view, RED, 1), _bump(view, YELLOW, 2)])]
