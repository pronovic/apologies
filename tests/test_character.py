# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access

from flexmock import flexmock

from apologies.character import Character


class TestCharacter:
    def test_constructor(self) -> None:
        source = flexmock()
        character = Character("c", source)
        assert character.name == "c"
        assert character.source is source

    def test_construct_move_minimal(self) -> None:
        source = flexmock()
        character = Character("c", source)
        game = flexmock()
        mode = flexmock()
        player = flexmock()
        flexmock(source).should_receive("construct_move").with_args(game, mode, player, None, False).once()
        character.construct_move(game, mode, player)

    def test_construct_move_all_args(self) -> None:
        source = flexmock()
        character = Character("c", source)
        game = flexmock()
        mode = flexmock()
        player = flexmock()
        card = flexmock()
        flexmock(source).should_receive("construct_move").with_args(game, mode, player, card, True).once()
        character.construct_move(game, mode, player, card, True)
