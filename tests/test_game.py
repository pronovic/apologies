# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=wildcard-import,no-self-use,protected-access
# Unit tests for game.py

import pytest
from apologies.game import *


class TestCard:
    def test_constructor(self) -> None:
        card = Card(0, "name")
        assert card.id == 0
        assert card.name == "name"


class TestDeck:
    def test_constructor(self) -> None:
        deck = Deck()

        assert len(deck._draw_pile.keys()) == DECK_SIZE
        assert len(deck._discard_pile.keys()) == 0

        cardcounts = {card: 0 for card in LEGAL_CARDS}
        for card in deck._draw_pile.values():
            cardcounts[card.name] += 1
        for name in LEGAL_CARDS:
            assert cardcounts[name] == DECK_COUNTS[name]

    def test_draw_and_discard(self) -> None:
        deck = Deck()

        # Check that we can draw the entire dec
        drawn = []
        for _ in range(DECK_SIZE):
            drawn.append(deck.draw())
        assert len(deck._draw_pile) == 0
        with pytest.raises(ValueError):
            deck.draw()

        # Discard one card and prove we can draw it
        card = drawn.pop()
        assert len(deck._discard_pile) == 0
        deck.discard(card)
        assert len(deck._discard_pile) == 1
        assert card is deck.draw()
        assert len(deck._discard_pile) == 0
        assert len(deck._draw_pile) == 0

        # Discard a few others and prove they can also be drawn
        deck.discard(drawn.pop())
        deck.discard(drawn.pop())
        deck.discard(drawn.pop())
        assert len(deck._discard_pile) == 3
        assert len(deck._draw_pile) == 0
        deck.draw()
        assert len(deck._discard_pile) == 0
        assert len(deck._draw_pile) == 2
        deck.draw()
        assert len(deck._discard_pile) == 0
        assert len(deck._draw_pile) == 1
        deck.draw()
        assert len(deck._discard_pile) == 0
        assert len(deck._draw_pile) == 0

        # Make sure the deck still gives us an error when empty
        with pytest.raises(ValueError):
            deck.draw()


# noinspection PyTypeHints
class TestPawn:
    def test_constructor(self) -> None:
        pawn = Pawn("color", 0)
        assert pawn.color == "color"
        assert pawn.index == 0
        assert pawn.name == "color-0"
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_constructor_with_name(self) -> None:
        pawn = Pawn("color", 0, name="whatever")
        assert pawn.color == "color"
        assert pawn.index == 0
        assert pawn.name == "whatever"
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_start(self) -> None:
        pawn = Pawn("color", 0)
        pawn.start = "x"  # type: ignore[assignment]
        pawn.home = "x"  # type: ignore[assignment]
        pawn.safe = "x"  # type: ignore[assignment]
        pawn.square = "x"  # type: ignore[assignment]
        pawn.move_to_start()
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_home(self) -> None:
        pawn = Pawn("color", 0)
        pawn.start = "x"  # type: ignore[assignment]
        pawn.home = "x"  # type: ignore[assignment]
        pawn.safe = "x"  # type: ignore[assignment]
        pawn.square = "x"  # type: ignore[assignment]
        pawn.move_to_home()
        assert pawn.start is False
        assert pawn.home is True
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_safe_valid(self) -> None:
        for square in range(SAFE_SQUARES):
            pawn = Pawn("color", 0)
            pawn.start = "x"  # type: ignore[assignment]
            pawn.home = "x"  # type: ignore[assignment]
            pawn.safe = "x"  # type: ignore[assignment]
            pawn.square = "x"  # type: ignore[assignment]
            pawn.move_to_safe(square)
            assert pawn.start is False
            assert pawn.home is False
            assert pawn.safe == square
            assert pawn.square is None

    def test_move_to_safe_invalid(self) -> None:
        for square in [-1000, -2 - 1, 5, 6, 1000]:
            with pytest.raises(ValueError):
                pawn = Pawn("color", 0)
                pawn.move_to_safe(square)

    def test_move_to_square_invalid(self) -> None:
        for square in [-1000, -2 - 1, 60, 61, 1000]:
            with pytest.raises(ValueError):
                pawn = Pawn("color", 0)
                pawn.move_to_square(square)


class TestPlayer:
    def test_constructor(self) -> None:
        player = Player("color")
        assert player.color == "color"
        assert player.name is None
        assert len(player.pawns) == PAWNS
        for pawn in player.pawns:
            assert isinstance(pawn, Pawn)


class TestGame:
    def test_constructor_2_players_standard(self) -> None:
        game = Game(2)
        assert game.started is False
        assert game.adult_mode is False
        assert len(game.players) == 2
        for color in [RED, YELLOW]:
            assert game.players[color].color == color
            assert len(game.players[color].hand) == 0
        assert game.deck is not None

    def test_constructor_3_players_standard(self) -> None:
        game = Game(3)
        assert game.started is False
        assert game.adult_mode is False
        assert len(game.players) == 3
        for color in [RED, YELLOW, GREEN]:
            assert game.players[color].color == color
            assert len(game.players[color].hand) == 0
        assert game.deck is not None

    def test_constructor_4_players_standard(self) -> None:
        game = Game(4)
        assert game.started is False
        assert game.adult_mode is False
        assert len(game.players) == 4
        for color in [RED, YELLOW, BLUE]:
            assert game.players[color].color == color
            assert len(game.players[color].hand) == 0
        assert game.deck is not None

    def test_constructor_invalid_players(self) -> None:
        for playercount in [-2, -1, 0, 1, 5, 6]:
            with pytest.raises(ValueError):
                Game(playercount)

    def test_set_adult_mode_started(self) -> None:
        game = Game(4)
        game._started = True
        with pytest.raises(ValueError):
            game.set_adult_mode()

    def test_set_adult_mode_notstarted(self) -> None:
        game = Game(4)
        game.set_adult_mode()
        for color in [RED, YELLOW, BLUE]:
            assert game.players[color].color == color
            assert game.players[color].pawns[0].start is True
            assert len(game.players[color].hand) == ADULT_HAND
