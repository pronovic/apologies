# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name,protected-access,broad-except
# Unit tests for source.py

import pytest
from mock import MagicMock

from apologies.game import GameMode
from apologies.source import RandomInputSource, source


class TestFunctions:
    def test_source_unknown(self):
        with pytest.raises(TypeError):
            source("apologies.game.Blah")  # not a valid class

    def test_source_invalid(self):
        with pytest.raises(ValueError):
            source("apologies.engine.Engine")  # valid class, but not a CharacterInputSource

    def test_source_valid(self):
        ris = source("apologies.source.RandomInputSource")
        assert isinstance(ris, RandomInputSource)


class TestRandomInputSource:
    def test_constructor(self):
        RandomInputSource()  # the contract says there must be a valid zero-args constructor

    def test_choose_move(self):
        move1 = MagicMock()
        move2 = MagicMock()
        move3 = MagicMock()
        legal_moves = [move1, move2, move3]
        ris = RandomInputSource()
        for _ in range(100):
            assert ris.choose_move(GameMode.ADULT, MagicMock(), legal_moves) in legal_moves
