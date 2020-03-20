# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name,protected-access
# Unit tests for engine.py

from flexmock import flexmock

from apologies.character import Character
from apologies.engine import Engine
from apologies.game import GameMode, PlayerColor


class TestEngine:
    def test_constructor(self) -> None:
        character1 = Character("one", flexmock())
        character2 = Character("two", flexmock())
        engine = Engine(GameMode.STANDARD, [character1, character2])
        assert engine.characters == [character1, character2]
        assert engine.mode == GameMode.STANDARD
        assert engine.started is False
        assert engine.completed is False
        assert len(engine._game.players) == 2
        assert engine._queue.entries == [PlayerColor.RED, PlayerColor.YELLOW]
        assert engine._rules.mode == GameMode.STANDARD

    def test_start_game(self) -> None:
        engine = TestEngine._create_engine()
        expected = flexmock()
        flexmock(engine._rules).should_receive("start_game").once().and_return(expected)
        assert engine.start_game() == expected

    @staticmethod
    def _create_engine() -> Engine:
        character1 = Character("one", flexmock())
        character2 = Character("two", flexmock())
        engine = Engine(GameMode.STANDARD, [character1, character2])
        engine._rules = flexmock()
        return engine
