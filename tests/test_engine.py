# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name,protected-access
# Unit tests for engine.py

from flexmock import flexmock

from apologies.character import Character
from apologies.engine import ADULT_HAND, Engine, _Player
from apologies.game import DECK_SIZE, GameMode, Player, PlayerColor


class TestPlayer:
    def test_constructor(self) -> None:
        gameplayer = Player(PlayerColor.BLUE)
        character = Character("one", flexmock())
        player = _Player(gameplayer, character)
        assert player.player is gameplayer
        assert player.character is character
        assert player.winner is False


class TestEngine:
    def test_constructor(self) -> None:
        character1 = Character("one", flexmock())
        character2 = Character("two", flexmock())
        engine = Engine([character1, character2], GameMode.STANDARD)
        assert engine.characters == [character1, character2]
        assert engine.mode == GameMode.STANDARD
        assert engine.started is False
        assert engine.completed is False
        assert len(engine._game.players) == 2
        assert engine._players == {
            PlayerColor.RED: _Player(engine._game.players[PlayerColor.RED], character1),
            PlayerColor.YELLOW: _Player(engine._game.players[PlayerColor.YELLOW], character2),
        }
        assert engine._queue.entries == [PlayerColor.RED, PlayerColor.YELLOW]

    def test_start_game_standard(self) -> None:
        character1 = Character("one", flexmock())
        character2 = Character("two", flexmock())
        engine = Engine([character1, character2], GameMode.STANDARD)
        engine.start_game()
        assert engine.started is True
        for color in [PlayerColor.RED, PlayerColor.YELLOW]:
            assert engine._game.players[color].color == color
            assert len(engine._game.players[color].hand) == 0

    def test_start_game_adult(self) -> None:
        character1 = Character("one", flexmock())
        character2 = Character("two", flexmock())
        engine = Engine([character1, character2], GameMode.ADULT)
        engine.start_game()
        assert engine.started is True
        assert len(engine._game.deck._draw_pile) == DECK_SIZE - (2 * ADULT_HAND)
        assert engine._game.players[PlayerColor.RED].color == PlayerColor.RED
        assert engine._game.players[PlayerColor.RED].pawns[0].square == 4
        assert len(engine._game.players[PlayerColor.RED].hand) == ADULT_HAND
        assert engine._game.players[PlayerColor.YELLOW].color == PlayerColor.YELLOW
        assert engine._game.players[PlayerColor.YELLOW].pawns[0].square == 34
        assert len(engine._game.players[PlayerColor.YELLOW].hand) == ADULT_HAND
