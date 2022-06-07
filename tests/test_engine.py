# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name,protected-access,broad-except,too-many-public-methods,assigning-non-slot
# Unit tests for engine.py

from unittest.mock import MagicMock, Mock, PropertyMock, call, patch

import pytest

from apologies.engine import Character, Engine
from apologies.game import Card, CardType, GameMode, PlayerColor
from apologies.rules import Action, ActionType, Move, Rules


class TestCharacter:
    def test_constructor(self):
        source = Mock()
        character = Character("c", source)
        assert character.name == "c"
        assert character.source is source

    # noinspection PyTypeChecker
    def test_choose_move_minimal(self):
        source = Mock()
        character = Character("c", source)
        mode = Mock()
        view = Mock()
        legal_moves = []
        evaluator = MagicMock()
        character.choose_move(mode, view, legal_moves, evaluator)
        source.choose_move.assert_called_once_with(mode, view, legal_moves, evaluator)

    # noinspection PyTypeChecker
    def test_choose_move_all_args(self):
        source = Mock()
        character = Character("c", source)
        mode = Mock()
        view = Mock()
        legal_moves = []
        evaluator = MagicMock()
        character.choose_move(mode, view, legal_moves, evaluator)
        source.choose_move.assert_called_once_with(mode, view, legal_moves, evaluator)


class TestEngine:
    def test_constructor_not_random(self):
        character1 = Character("one", Mock())
        character2 = Character("two", Mock())
        engine = Engine(GameMode.STANDARD, [character1, character2], first=PlayerColor.RED)  # 1st player deterministic
        assert engine.players == 2
        assert engine.characters == [character1, character2]
        assert engine.mode == GameMode.STANDARD
        assert engine.started is False
        assert engine.completed is False
        assert engine.state == "Game waiting to start"
        assert engine.game is engine._game
        assert len(engine._game.players) == 2
        assert engine.first == PlayerColor.RED
        assert engine._queue.first == engine.first
        assert engine._queue.entries == [PlayerColor.RED, PlayerColor.YELLOW]
        assert engine._rules.mode == GameMode.STANDARD
        assert engine.colors == engine._map and engine.colors is not engine._map  # it's a copy
        assert engine._map == {PlayerColor.RED: character1, PlayerColor.YELLOW: character2}

    def test_constructor_random(self):
        found = []
        for _ in range(0, 100):
            character1 = Character("one", Mock())
            character2 = Character("two", Mock())
            character3 = Character("three", Mock())
            character4 = Character("four", Mock())
            engine = Engine(GameMode.STANDARD, [character1, character2, character3, character4])  # 1st player random
            assert engine.players == 4
            assert engine.characters == [character1, character2, character3, character4]
            assert engine.mode == GameMode.STANDARD
            assert engine.started is False
            assert engine.completed is False
            assert engine.state == "Game waiting to start"
            assert engine.game is engine._game
            assert len(engine._game.players) == 4
            assert engine.first in [PlayerColor.RED, PlayerColor.YELLOW, PlayerColor.GREEN, PlayerColor.BLUE]
            assert engine._queue.first == engine.first
            assert engine._queue.entries == [PlayerColor.RED, PlayerColor.YELLOW, PlayerColor.GREEN, PlayerColor.BLUE]
            assert engine._rules.mode == GameMode.STANDARD
            assert engine.colors == engine._map and engine.colors is not engine._map  # it's a copy
            assert engine._map == {
                PlayerColor.RED: character1,
                PlayerColor.YELLOW: character2,
                PlayerColor.GREEN: character3,
                PlayerColor.BLUE: character4,
            }
            found.append(engine.first)
        # check that all players showed up as the first player at least once
        assert PlayerColor.RED in found
        assert PlayerColor.YELLOW in found
        assert PlayerColor.BLUE in found
        assert PlayerColor.GREEN in found

    def test_started(self):
        engine = TestEngine._create_engine()
        with patch("apologies.game.Game.started", new_callable=PropertyMock) as started:
            started.return_value = False
            assert engine.started is False
            assert engine.state == "Game waiting to start"
            started.return_value = True
            assert engine.started is True
            assert engine.state == "Game in progress"

    def test_completed(self):
        engine = TestEngine._create_engine()
        with patch("apologies.game.Game.completed", new_callable=PropertyMock) as completed:
            completed.return_value = False
            assert engine.completed is False
            assert engine.state == "Game in progress"
            completed.return_value = True
            assert engine.completed is True
            assert engine.state == "Game completed"

    def test_winner(self):
        engine = TestEngine._create_engine()
        game_winner = MagicMock(color=PlayerColor.YELLOW)
        with patch("apologies.game.Game.completed", new_callable=PropertyMock) as completed:
            with patch("apologies.game.Game.winner", new_callable=PropertyMock) as winner:
                winner.return_value = game_winner
                completed.return_value = False
                assert engine.winner() is None
                completed.return_value = True
                assert engine.winner() == (engine._map[PlayerColor.YELLOW], game_winner)

    def test_reset(self):
        engine = TestEngine._create_engine()
        saved = engine._game
        engine.reset()
        assert engine._game is not None and engine._game is not saved and not engine._game.started

    def test_start_game(self):
        engine = TestEngine._create_engine()
        engine._rules.start_game = MagicMock()
        assert engine.start_game() == engine._game
        engine._rules.start_game.assert_called_once_with(engine._game)

    def test_draw(self):
        engine = TestEngine._create_engine()

        card = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=card)

        assert card is engine.draw()

    def test_discard(self):
        engine = TestEngine._create_engine()

        card = MagicMock()
        engine._game.deck.discard = MagicMock()

        engine.discard(card)
        engine._game.deck.discard.assert_called_once_with(card)

    def test_construct_legal_moves_standard_nocard(self):
        engine = TestEngine._create_engine(mode=GameMode.STANDARD)

        view = Mock()
        drawcard = Mock()
        movecard = Card(0, CardType.CARD_1)
        move = Move(movecard, [])
        legal_moves = [move]
        engine._game.deck.draw = MagicMock(return_value=drawcard)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)

        assert engine.construct_legal_moves(view) == (drawcard, legal_moves)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=drawcard)

    def test_construct_legal_moves_standard_card(self):
        engine = TestEngine._create_engine(mode=GameMode.STANDARD)

        view = Mock()
        providedcard = Mock()
        drawcard = Mock()
        movecard = Card(0, CardType.CARD_1)
        move = Move(movecard, [])
        legal_moves = [move]
        engine._game.deck.draw = MagicMock(return_value=drawcard)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)

        assert engine.construct_legal_moves(view, card=providedcard) == (providedcard, legal_moves)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=providedcard)
        engine._game.deck.draw.assert_not_called()

    def test_construct_legal_moves_adult_nocard(self):
        engine = TestEngine._create_engine(mode=GameMode.ADULT)

        view = Mock()
        drawcard = Mock()
        movecard = Card(0, CardType.CARD_1)
        move = Move(movecard, [])
        legal_moves = [move]
        engine._game.deck.draw = MagicMock(return_value=drawcard)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)

        assert engine.construct_legal_moves(view) == (None, legal_moves)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=None)
        engine._game.deck.draw.assert_not_called()

    def test_construct_legal_moves_adult_card(self):
        engine = TestEngine._create_engine(mode=GameMode.ADULT)

        view = Mock()
        providedcard = Mock()
        drawcard = Mock()
        movecard = Card(0, CardType.CARD_1)
        move = Move(movecard, [])
        legal_moves = [move]
        engine._game.deck.draw = MagicMock(return_value=drawcard)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)

        assert engine.construct_legal_moves(view, card=providedcard) == (providedcard, legal_moves)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=providedcard)
        engine._game.deck.draw.assert_not_called()

    def test_play_next_completed(self):
        engine = TestEngine._create_engine()
        with patch("apologies.game.Game.completed", new_callable=PropertyMock) as completed:
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

        card = Card(0, CardType.CARD_1)
        player = engine._game.players[PlayerColor.RED]
        view = Mock()
        move = Move(card, [])
        legal_moves = [move]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=card)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(return_value=move)

        engine.play_next()

        engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=card)
        engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
        engine._game.track.assert_called_once_with("Turn is forfeit; discarded card 1", player, card)
        engine._game.deck.discard.assert_called_once_with(card)

    def test_play_next_standard_illegal(self):
        engine = TestEngine._create_engine()

        card = Card(0, CardType.CARD_12)
        player = engine._game.players[PlayerColor.RED]
        pawn = player.pawns[0]
        view = Mock()
        move = Move(card, [Action(ActionType.MOVE_TO_START, Mock())])  # not found in legal_moves
        legal_moves = [Move(card, [Action(ActionType.MOVE_TO_POSITION, pawn)])]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=card)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(return_value=move)
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(return_value=False)

        engine.play_next()

        engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=card)
        engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
        engine._rules.execute_move.assert_called_once_with(engine._game, player, legal_moves[0])  # we choose random move
        engine._game.deck.discard.assert_called_once_with(card)
        engine._rules.draw_again.assert_called_once_with(card)

    def test_play_next_standard_legal(self):
        engine = TestEngine._create_engine()

        card = Card(0, CardType.CARD_12)
        player = engine._game.players[PlayerColor.RED]
        pawn = player.pawns[0]
        view = Mock()
        move = Move(card, [Action(ActionType.MOVE_TO_START, pawn)])
        legal_moves = [move]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=card)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(return_value=move)
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(return_value=False)

        engine.play_next()

        engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=card)
        engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
        engine._rules.execute_move.assert_called_once_with(engine._game, player, move)
        engine._game.deck.discard.assert_called_once_with(card)
        engine._rules.draw_again.assert_called_once_with(card)

    def test_play_next_standard_draw_again(self):
        engine = TestEngine._create_engine()

        card1 = Card(0, CardType.CARD_12)
        card2 = Card(1, CardType.CARD_10)
        player = engine._game.players[PlayerColor.RED]
        pawn = player.pawns[0]
        view = Mock()
        move1 = Move(card1, [Action(ActionType.MOVE_TO_START, pawn)])
        move2 = Move(card2, [Action(ActionType.MOVE_TO_POSITION, pawn)])
        legal_moves1 = [move1]
        legal_moves2 = [move2]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(side_effect=[legal_moves1, legal_moves2])
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(side_effect=[card1, card2])
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(side_effect=[move1, move2])
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(side_effect=[True, False])

        engine.play_next()

        engine._game.create_player_view.assert_has_calls([call(PlayerColor.RED), call(PlayerColor.RED)])
        engine._rules.construct_legal_moves.assert_has_calls([call(view, card=card1), call(view, card=card2)])
        engine.characters[0].choose_move.assert_has_calls(
            [call(engine.mode, view, legal_moves1, Rules.evaluate_move), call(engine.mode, view, legal_moves2, Rules.evaluate_move)]
        )
        engine._rules.execute_move.assert_has_calls([call(engine._game, player, move1), call(engine._game, player, move2)])
        engine._game.deck.discard.assert_has_calls([call(card1), call(card2)])
        engine._rules.draw_again.assert_has_calls([call(card1), call(card2)])

    def test_play_next_standard_complete(self):
        with patch("apologies.game.Game.completed", new_callable=PropertyMock) as completed:
            completed.side_effect = [False, True]  # not complete when we start execution, but complete after the 1st move

            engine = TestEngine._create_engine()

            card = Card(0, CardType.CARD_12)
            player = engine._game.players[PlayerColor.RED]
            pawn = player.pawns[0]
            view = Mock()
            move = Move(card, [Action(ActionType.MOVE_TO_START, pawn)])
            legal_moves = [move]

            engine._game.create_player_view = MagicMock(return_value=view)
            engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
            engine._game.track = MagicMock()
            engine._game.deck.draw = MagicMock(return_value=card)
            engine._game.deck.discard = MagicMock()
            engine.characters[0].choose_move = MagicMock(return_value=move)
            engine._rules.execute_move = MagicMock()
            engine._rules.draw_again = MagicMock(return_value=True)  # we won't check this because the complete flag is set

            engine.play_next()

            engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
            engine._rules.construct_legal_moves.assert_called_once_with(view, card=card)
            engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
            engine._rules.execute_move.assert_called_once_with(engine._game, player, move)
            engine._game.deck.discard.assert_called_once_with(card)
            engine._rules.draw_again.assert_not_called()

    def test_play_next_adult_forfeit(self):
        engine = TestEngine._create_engine(GameMode.ADULT)

        player = engine._game.players[PlayerColor.RED]
        view = Mock()
        movecard = player.hand[0]
        replacementcard = Card(999, CardType.CARD_APOLOGIES)
        move = Move(movecard, [])
        legal_moves = [move]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=replacementcard)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(return_value=move)

        engine.play_next()

        engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=None)
        engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
        engine._game.track.assert_called_once_with("Turn is forfeit; discarded card %s" % movecard.cardtype.value, player, movecard)
        engine._game.deck.discard.assert_called_once_with(movecard)

        assert movecard not in player.hand
        assert replacementcard in player.hand

    def test_play_next_adult_illegal(self):
        engine = TestEngine._create_engine(GameMode.ADULT)

        player = engine._game.players[PlayerColor.RED]
        pawn = player.pawns[0]
        view = Mock()
        movecard = player.hand[0]
        replacementcard = Card(999, CardType.CARD_APOLOGIES)
        move = Move(movecard, [Action(ActionType.MOVE_TO_START, Mock())])  # not found in legal_moves
        legal_moves = [Move(movecard, [Action(ActionType.MOVE_TO_POSITION, pawn)])]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=replacementcard)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(return_value=move)
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(return_value=False)

        engine.play_next()

        engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=None)
        engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
        engine._rules.execute_move.assert_called_once_with(engine._game, player, legal_moves[0])  # we choose random move
        engine._game.deck.discard.assert_called_once_with(movecard)
        engine._rules.draw_again.assert_called_once_with(movecard)

        assert movecard not in player.hand
        assert replacementcard in player.hand

    def test_play_next_adult_legal(self):
        engine = TestEngine._create_engine(GameMode.ADULT)

        player = engine._game.players[PlayerColor.RED]
        pawn = player.pawns[0]
        view = Mock()
        movecard = player.hand[0]
        replacementcard = Card(999, CardType.CARD_APOLOGIES)
        move = Move(movecard, [Action(ActionType.MOVE_TO_START, pawn)])
        legal_moves = [move]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(return_value=replacementcard)
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(return_value=move)
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(return_value=False)

        engine.play_next()

        engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
        engine._rules.construct_legal_moves.assert_called_once_with(view, card=None)
        engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
        engine._rules.execute_move.assert_called_once_with(engine._game, player, move)
        engine._game.deck.discard.assert_called_once_with(movecard)
        engine._rules.draw_again.assert_called_once_with(movecard)

        assert movecard not in player.hand
        assert replacementcard in player.hand

    def test_play_next_adult_draw_again(self):
        engine = TestEngine._create_engine(GameMode.ADULT)

        player = engine._game.players[PlayerColor.RED]
        pawn = player.pawns[0]
        view = Mock()
        movecard1 = player.hand[0]
        movecard2 = player.hand[1]
        replacementcard1 = Card(998, CardType.CARD_APOLOGIES)
        replacementcard2 = Card(999, CardType.CARD_APOLOGIES)
        move1 = Move(movecard1, [Action(ActionType.MOVE_TO_START, pawn)])
        move2 = Move(movecard2, [Action(ActionType.MOVE_TO_POSITION, pawn)])
        legal_moves1 = [move1]
        legal_moves2 = [move2]

        engine._game.create_player_view = MagicMock(return_value=view)
        engine._rules.construct_legal_moves = MagicMock(side_effect=[legal_moves1, legal_moves2])
        engine._game.track = MagicMock()
        engine._game.deck.draw = MagicMock(side_effect=[replacementcard1, replacementcard2])
        engine._game.deck.discard = MagicMock()
        engine.characters[0].choose_move = MagicMock(side_effect=[move1, move2])
        engine._rules.execute_move = MagicMock()
        engine._rules.draw_again = MagicMock(side_effect=[True, False])

        engine.play_next()

        engine._game.create_player_view.assert_has_calls([call(PlayerColor.RED), call(PlayerColor.RED)])
        engine._rules.construct_legal_moves.assert_has_calls([call(view, card=None), call(view, card=None)])
        engine.characters[0].choose_move.assert_has_calls(
            [call(engine.mode, view, legal_moves1, Rules.evaluate_move), call(engine.mode, view, legal_moves2, Rules.evaluate_move)]
        )
        engine._rules.execute_move.assert_has_calls([call(engine._game, player, move1), call(engine._game, player, move2)])
        engine._game.deck.discard.assert_has_calls([call(movecard1), call(movecard2)])
        engine._rules.draw_again.assert_has_calls([call(movecard1), call(movecard2)])

        assert movecard1 not in player.hand
        assert movecard2 not in player.hand
        assert replacementcard1 in player.hand
        assert replacementcard2 in player.hand

    def test_play_next_adult_draw_again_complete(self):
        with patch("apologies.game.Game.completed", new_callable=PropertyMock) as completed:
            completed.side_effect = [False, True]  # not complete when we start execution, but complete after the 1st move

            engine = TestEngine._create_engine(GameMode.ADULT)

            player = engine._game.players[PlayerColor.RED]
            pawn = player.pawns[0]
            view = Mock()
            movecard = player.hand[0]
            replacementcard = Card(999, CardType.CARD_APOLOGIES)
            move = Move(movecard, [Action(ActionType.MOVE_TO_START, pawn)])
            legal_moves = [move]

            engine._game.create_player_view = MagicMock(return_value=view)
            engine._rules.construct_legal_moves = MagicMock(return_value=legal_moves)
            engine._game.track = MagicMock()
            engine._game.deck.draw = MagicMock(return_value=replacementcard)
            engine._game.deck.discard = MagicMock()
            engine.characters[0].choose_move = MagicMock(return_value=move)
            engine._rules.execute_move = MagicMock()
            engine._rules.draw_again = MagicMock(return_value=True)  # we won't check this because the complete flag is set

            engine.play_next()

            engine._game.create_player_view.assert_called_once_with(PlayerColor.RED)
            engine._rules.construct_legal_moves.assert_called_once_with(view, card=None)
            engine.characters[0].choose_move.assert_called_once_with(engine.mode, view, legal_moves, Rules.evaluate_move)
            engine._rules.execute_move.assert_called_once_with(engine._game, player, move)
            engine._game.deck.discard.assert_called_once_with(movecard)
            engine._rules.draw_again.assert_not_called()

            assert movecard not in player.hand
            assert replacementcard in player.hand

    @staticmethod
    def _create_engine(mode: GameMode = GameMode.STANDARD) -> Engine:
        character1 = Character("character1", Mock())
        character1.choose_move = MagicMock()  # type: ignore

        character2 = Character("character2", Mock())
        character1.choose_move = MagicMock()  # type: ignore

        first = PlayerColor.RED
        engine = Engine(mode, [character1, character2], first=first)
        engine.start_game()

        return engine
