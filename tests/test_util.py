# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name
# Unit tests for cli.py

import pytest
from apologies.util import CircularQueue


class TestCircularQueue:
    def test_constructor_empty(self) -> None:
        with pytest.raises(ValueError):
            CircularQueue([])

    def test_constructor_single(self) -> None:
        queue = CircularQueue(["a"])
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"

    def test_constructor_multiple(self) -> None:
        queue = CircularQueue(["a", "b", "c",])
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
