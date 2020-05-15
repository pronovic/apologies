# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name,not-callable

import pytest

from apologies.util import CircularQueue


class TestCircularQueue:
    def test_constructor_empty(self):
        with pytest.raises(ValueError):
            CircularQueue([])

    def test_constructor_single(self):
        queue = CircularQueue(["a"])
        assert queue.entries == ["a"]
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"
        assert queue.next() == "a"

    def test_constructor_single_none(self):
        queue = CircularQueue([None])
        assert queue.entries == [None]
        assert queue.next() is None
        assert queue.next() is None
        assert queue.next() is None
        assert queue.next() is None
        assert queue.next() is None
        assert queue.next() is None

    def test_constructor_multiple(self):
        queue = CircularQueue(["a", "b", "c", "d", "e", None])
        assert queue.entries == ["a", "b", "c", "d", "e", None]
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
        assert queue.next() == "d"
        assert queue.next() == "e"
        assert queue.next() is None
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
        assert queue.next() == "d"
        assert queue.next() == "e"
        assert queue.next() is None
        assert queue.next() == "a"

    def test_constructor_multiple_first(self):
        queue = CircularQueue(["a", "b", "c", "d", "e", None], first="c")
        assert queue.entries == ["a", "b", "c", "d", "e", None]
        assert queue.next() == "c"
        assert queue.next() == "d"
        assert queue.next() == "e"
        assert queue.next() is None
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
        assert queue.next() == "d"
        assert queue.next() == "e"
        assert queue.next() is None
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"

    def test_constructor_multiple_first_none(self):
        queue = CircularQueue(["a", "b", "c", "d", "e", None], first=None)
        assert queue.entries == ["a", "b", "c", "d", "e", None]
        assert queue.next() is None
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
        assert queue.next() == "d"
        assert queue.next() == "e"
        assert queue.next() is None
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
        assert queue.next() == "d"
        assert queue.next() == "e"
        assert queue.next() is None

    def test_constructor_first_invalid(self):
        with pytest.raises(ValueError):
            CircularQueue([], first=None)
        with pytest.raises(ValueError):
            CircularQueue([], first="")
        with pytest.raises(ValueError):
            CircularQueue([], first="f")
        with pytest.raises(ValueError):
            CircularQueue(["a"], first=None)
        with pytest.raises(ValueError):
            CircularQueue(["a"], first="")
        with pytest.raises(ValueError):
            CircularQueue(["a"], first="f")
        with pytest.raises(ValueError):
            CircularQueue(["a", "b", "c", "d", "e"], first=None)
        with pytest.raises(ValueError):
            CircularQueue(["a", "b", "c", "d", "e"], first="")
        with pytest.raises(ValueError):
            CircularQueue(["a", "b", "c", "d", "e"], first="f")
