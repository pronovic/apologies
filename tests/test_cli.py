# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=redefined-outer-name
# Unit tests for cli.py

import os
from typing import Dict

import pytest
from flexmock import flexmock

from apologies.cli import _example, _lookup_method, _render, cli

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures/test_cli")


@pytest.fixture
def data() -> Dict[str, str]:
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

    def test_lookup_method(self) -> None:
        assert _lookup_method("example") is _example
        assert _lookup_method("render") is _render
        with pytest.raises(AttributeError):
            assert _lookup_method("")
        with pytest.raises(AttributeError):
            assert _lookup_method("bogus")

    def test_example(self) -> None:
        argv = ["1", "a", "b"]
        stdout = flexmock(write=lambda x: None)
        stderr = flexmock(write=lambda x: None)
        flexmock(stdout).should_receive("write").with_args("Hello, stdout: 1\n").once()
        flexmock(stderr).should_receive("write").with_args("Hello, stderr: 1\n").once()
        _example(argv, stdout, stderr)

    def test_main(self) -> None:
        cli("example")  # Just make sure it doesn't blow up


class TestRender:
    """
    Unit tests for the render script.
    """

    def test_render(self, data: Dict[str, str]) -> None:
        stdout = flexmock(write=lambda x: None)
        flexmock(stdout).should_receive("write").with_args(data["render"]).once()
        _render(flexmock(), stdout, flexmock())
