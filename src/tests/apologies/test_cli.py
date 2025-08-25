# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name

import os
from unittest.mock import MagicMock

import pytest

from apologies.cli import _lookup_method, cli, example, render

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures/test_cli")


@pytest.fixture
def data():
    data = {}
    for f in os.listdir(FIXTURE_DIR):
        p = os.path.join(FIXTURE_DIR, f)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as r:
                data[f] = r.read()
    return data


class TestCli:
    """
    General unit tests for the CLI interface.
    """

    def test_lookup_method(self):
        assert _lookup_method("example") is example
        assert _lookup_method("render") is render
        with pytest.raises(AttributeError):
            assert _lookup_method("")
        with pytest.raises(AttributeError):
            assert _lookup_method("bogus")

    def test_example(self):
        argv = ["1", "a", "b"]
        stdout = MagicMock()
        stderr = MagicMock()
        example(argv, stdout, stderr)
        stdout.write.assert_called_once_with("Hello, stdout: 1\n")
        stderr.write.assert_called_once_with("Hello, stderr: 1\n")

    def test_main(self):
        cli("example")  # just make sure it doesn't blow up


class TestRender:
    """
    Unit tests for the render script.
    """

    def test_render(self, data):
        stdout = MagicMock()
        render(MagicMock(), stdout, MagicMock())
        stdout.write.assert_called_once_with(data["render"])
