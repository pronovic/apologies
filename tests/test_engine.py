# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name,protected-access,broad-except
# Unit tests for engine.py

import mock
import pytest
from mock import MagicMock, Mock, call

from apologies.engine import Character, Engine
from apologies.game import Card, CardType, GameMode, PlayerColor
from apologies.rules import Action, ActionType, Move, ValidationError


class TestCharacter:
    def test_constructor(self):
        source = Mock()
        character = Character("c", source)
        assert character.name == "c"
        assert character.source is source

    def test_construct_move_minimal(self):
        source = Mock()
        character = Character("c", source)
        game = Mock()
        mode = Mock()
        player = Mock()
        character.construct_move(game, mode, player)
        source.construct_move.assert_called_once_with(game, mode, player, None, False)

    def test_construct_move_all_args(self):
        source = Mock()
        character = Character("c", source)
        game = Mock()
        mode = Mock()
        player = Mock()
        card = Mock()
        character.construct_move(game, mode, player, card, True)
        source.construct_move.assert_called_once_with(game, mode, player, card, True)


class TestEngine:
    def test_constructor(self):
        character1 = Character("one", Mock())
        character2 = Character("two", Mock())
        engine = Engine(GameMode.STANDARD, [character1, character2])
        assert engine.characters == [character1, character2]
        assert engine.mode == GameMode.STANDARD
        assert engine.started is False
        assert engine.completed is False
        assert len(engine._game.players) == 2
        assert engine._queue.entries == [PlayerColor.RED, PlayerColor.YELLOW]
        assert engine._rules.mode == GameMode.STANDARD
        assert engine._map == {PlayerColor.RED: character1, PlayerColor.YELLOW: character2}

    def test_started(self):
        engine = TestEngine._create_engine()
        with mock.patch("apologies.game.Game.started", new_callable=mock.PropertyMock) as started:
            started.return_value = False
            assert engine.started is False
            started.return_value = True
            assert engine.started is True

    def test_completed(self):
        engine = TestEngine._create_engine()
        with mock.patch("apologies.game.Game.completed", new_callable=mock.PropertyMock) as completed:
            completed.return_value = False
            assert engine.completed is False
            completed.return_value = True
            assert engine.completed is True

    def test_start_game(self):
        engine = TestEngine._create_engine()
        engine._rules.start_game = MagicMock()
        assert engine.start_game() == engine._game
        engine._rules.start_game.assert_called_once_with(engine._game)

    def test_play_next_completed(self):
        engine = TestEngine._create_engine()
        with mock.patch("apologies.game.Game.completed", new_callable=mock.PropertyMock) as completed:
            completed.return_value = True
            with pytest.raises(ValueError):
                engine.play_next()

    def test_play_next_failed(self):
        engine = TestEngine._create_engine()

        exception = Exception("Hello")
        copy = Mock()

        engine._queue.next = MagicMock(side_effect=exception)
        engine._game.copy = MagicMock(return_value=copy)

        try:
            engine.play_next()
        except Exception:
            assert engine._game is copy  # we replace with a copy of original if method raises exception

    def test_play_next_standard_forfeit(self):
        engine = TestEngine._create_engine()

        card = Card(0, "whatever")
        player = engine._game.players[PlayerColor.RED]
        move = Move(card, [])

        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=card)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].construct_move = MagicMock(return_value=move)

        engine.play_next()

        engine.characters[0].construct_move.assert_called_once_with(engine._game, engine.mode, player, card=card, invalid=False)
        engine._game.track.assert_called_once_with("Turn forfeited", player)
        engine._game.deck.discard.assert_called_once_with(card)

    def test_play_next_standard_invalid(self):
        engine = TestEngine._create_engine()

        card = Card(0, CardType.CARD_12)
        player = engine._game.players[PlayerColor.RED]
        exception = ValidationError("Hello")
        copy = Mock()
        move1 = Move(card, [Action(ActionType.BUMP_TO_START, Mock())])
        move2 = Move(card, [Action(ActionType.CHANGE_PLACES, Mock())])

        def execute_mock_stub(*args):
            if args[2] is move1:
                raise exception
            return mock.DEFAULT

        # note: I wanted to return two different copies, but that broke the test for some reason; I gave up
        engine._game.track = MagicMock()
        engine._game.copy = MagicMock(return_value=copy)
        engine._game.deck.draw = MagicMock(return_value=card)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].construct_move = MagicMock(side_effect=[move1, move2])
        engine._rules.execute_move = MagicMock(side_effect=execute_mock_stub)
        engine._rules.draw_again = MagicMock(return_value=False)

        engine.play_next()

        engine._game.track.called_once_with("Requested move was invalid", player)
        engine._game.deck.discard.assert_called_once_with(card)
        engine._rules.draw_again.assert_called_once_with(card)
        engine.characters[0].construct_move.assert_has_calls(
            [
                call(engine._game, engine.mode, player, card=card, invalid=False),
                call(engine._game, engine.mode, player, card=card, invalid=True),
            ]
        )
        engine._rules.execute_move.has_calls(
            [call(copy, PlayerColor.RED, move1), call(copy, PlayerColor.RED, move2), call(engine._game, PlayerColor.RED, move2),]
        )

    def test_play_next_standard_valid(self):
        engine = TestEngine._create_engine()

        card = Card(0, CardType.CARD_12)
        player = engine._game.players[PlayerColor.RED]
        copy = Mock()
        move = Move(card, [Action(ActionType.BUMP_TO_START, Mock())])

        engine._game.track = MagicMock()
        engine._game.copy = MagicMock(return_value=copy)
        engine._game.deck.draw = MagicMock(return_value=card)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].construct_move = MagicMock(return_value=move)
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(return_value=False)

        engine.play_next()

        engine._game.track.called_once_with("Requested move was invalid", player)
        engine._game.deck.discard.assert_called_once_with(card)
        engine.characters[0].construct_move.assert_called_once_with(engine._game, engine.mode, player, card=card, invalid=False)
        engine._rules.draw_again.assert_called_once_with(card)
        engine._rules.execute_move.has_calls(
            [call(copy, PlayerColor.RED, move), call(engine._game, PlayerColor.RED, move),]
        )

    def test_play_next_standard_draw_again(self):
        engine = TestEngine._create_engine()

        card1 = Card(0, CardType.CARD_12)
        card2 = Card(1, CardType.CARD_10)
        move1 = Move(card1, [Mock()])
        move2 = Move(card2, [Mock()])
        player = engine._game.players[PlayerColor.RED]
        copy = Mock()
        move1 = Move(card1, [Action(ActionType.BUMP_TO_START, Mock())])
        move2 = Move(card2, [Action(ActionType.CHANGE_PLACES, Mock())])

        engine._game.track = MagicMock()
        engine._game.copy = MagicMock(return_value=copy)
        engine._game.deck.draw = MagicMock(side_effect=[card1, card2])
        engine._game.deck.discard = MagicMock()
        engine.characters[0].construct_move = MagicMock(side_effect=[move1, move2])
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(side_effect=[True, False])

        engine.play_next()

        engine._game.deck.discard.has_calls([call(card1), call(card2)])
        engine.characters[0].construct_move.assert_has_calls(
            [
                call(engine._game, engine.mode, player, card=card1, invalid=False),
                call(engine._game, engine.mode, player, card=card2, invalid=False),
            ]
        )
        engine._rules.draw_again.has_calls([call(card1), call(card2)])
        engine._rules.execute_move.has_calls(
            [
                call(copy, PlayerColor.RED, move1),
                call(engine._game, PlayerColor.RED, move1),
                call(copy, PlayerColor.RED, move2),
                call(engine._game, PlayerColor.RED, move2),
            ]
        )

    def test_play_next_standard_draw_complete(self):
        engine = TestEngine._create_engine()

        card = Card(0, CardType.CARD_12)
        move = Move(card, [Mock()])
        player = engine._game.players[PlayerColor.RED]
        copy = Mock()
        move = Move(card, [Action(ActionType.BUMP_TO_START, Mock())])

        with mock.patch("apologies.game.Game.completed", new_callable=mock.PropertyMock) as completed:
            completed.side_effect = [False, True]

            engine._game.track = MagicMock()
            engine._game.copy = MagicMock(return_value=copy)
            engine._game.deck.draw = MagicMock(return_value=card)
            engine._game.deck.discard = MagicMock()
            engine.characters[0].construct_move = MagicMock(return_value=move)
            engine._rules.execute_move = MagicMock()
            engine._rules.draw_again = MagicMock()

            engine.play_next()

            engine._game.track.called_once_with("Requested move was invalid", player)
            engine._game.deck.discard.assert_called_once_with(card)
            engine.characters[0].construct_move.assert_called_once_with(engine._game, engine.mode, player, card=card, invalid=False)
            engine._rules.draw_again.assert_not_called()
            engine._rules.execute_move.has_calls(
                [call(copy, PlayerColor.RED, move), call(engine._game, PlayerColor.RED, move),]
            )

    def test_play_next_adult_forfeit(self):
        pass
        # engine = TestEngine._create_engine(mode=GameMode.ADULT)
        #
        # card = Card(0, "whatever")
        # player = engine._game.players[PlayerColor.RED]
        # move = Move(card, [])
        #
        # engine._game.track = MagicMock()
        # engine._game.deck.draw = MagicMock(return_value=card)
        # engine._game.deck.discard = MagicMock()
        # engine.characters[0].construct_move = MagicMock(return_value=move)
        #
        # engine.play_next()
        #
        # engine.characters[0].construct_move.assert_called_once_with(
        #     engine._game, engine.mode, player, card=card, invalid=False
        # )
        # engine._game.track.assert_called_once_with("Turn forfeited", player)
        # engine._game.deck.discard.assert_called_once_with(card)

    def test_play_next_adult_invalid(self):
        pytest.fail("Not implemented")

    def test_play_next_adult_valid(self):
        pytest.fail("Not implemented")

    def test_play_next_adult_draw_again(self):
        pytest.fail("Not implemented")

    def test_play_next_adult_draw_again_complete(self):
        pytest.fail("Not implemented")

    @staticmethod
    def _create_engine(mode: GameMode = GameMode.STANDARD) -> Engine:
        character1 = Character("character1", Mock())
        character1.construct_move = MagicMock()  # type: ignore

        character2 = Character("character2", Mock())
        character1.construct_move = MagicMock()  # type: ignore

        engine = Engine(mode, [character1, character2])
        engine.start_game()

        return engine
