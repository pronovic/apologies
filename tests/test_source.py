# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name,protected-access,broad-except
# Unit tests for source.py

from unittest.mock import MagicMock

import pytest

from apologies.game import GameMode
from apologies.reward import RewardCalculatorV1
from apologies.source import RandomInputSource, RewardV1InputSource, source


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
            assert ris.choose_move(GameMode.ADULT, MagicMock(), legal_moves, MagicMock()) in legal_moves


class TestRewardV1InputSource:
    def test_constructor(self):
        ris = RewardV1InputSource()  # the contract says there must be a valid zero-args constructor
        assert isinstance(ris.calculator, RewardCalculatorV1)

    def test_choose_move(self):
        view = MagicMock()

        move1 = MagicMock()
        move2 = MagicMock()
        move3 = MagicMock()
        legal_moves = [move1, move2, move3]

        ris = RewardV1InputSource()

        ris.calculator.calculate = MagicMock(side_effect=[200, 300, 100])
        evaluator = MagicMock(side_effect=[1, 2, 3])

        assert ris.choose_move(GameMode.ADULT, view, legal_moves, evaluator) is move2
