# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name

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

    def test_constructor_multiple(self):
        queue = CircularQueue(["a", "b", "c"])
        assert queue.entries == ["a", "b", "c"]
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
        assert queue.next() == "a"
        assert queue.next() == "b"
        assert queue.next() == "c"
