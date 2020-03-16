# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=wildcard-import,no-self-use
# Unit tests for game.py

import pytest
from apologies.game import *

# Unit tests for Card
class TestCard:
    def test_constructor(self):
        card = Card(0, "name")
        assert card.id == 0
        assert card.name == "name"

    def test_repr(self):
        Card(0, "name").__repr__()  # just make sure it doesn't blow up


# Unit tests for Hand
class TestHand:
    def test_constructor_nocards(self):
        hand = Hand()
        assert len(hand) == 0

    def test_constructor_cards(self):
        cards = [Card(0, "1"), Card(1, "12")]
        hand = Hand(cards)
        assert len(cards) == len(hand)
        assert cards[0] == hand[0]
        assert cards[1] == hand[1]

    def test_repr_nocards(self):
        Hand().__repr__()  # just make sure it doesn't blow up

    def test_repr_cards(self):
        cards = [Card(0, "1"), Card(1, "12")]
        Hand(cards).__repr__()  # just make sure it doesn't blow up


# Unit tests for Deck
class TestDeck:
    def test_constructor(self):
        deck = Deck()
        assert len(deck) == DECK_SIZE

    def test_repr(self):
        Deck().__repr__()  # just make sure it doesn't blow up

    def test_iterator(self):
        i = Deck().__iter__()
        for card in range(DECK_SIZE):
            assert isinstance(i.__next__(), Card)
        with pytest.raises(StopIteration):
            i.__next__()

    def test_draw_all(self):
        deck = Deck()
        expected = DECK_SIZE
        for _ in range(DECK_SIZE):
            deck.draw()
            expected -= 1
            assert len(deck) == expected
            assert len(deck) == deck.remaining()
        with pytest.raises(ValueError):
            deck.draw()

    def test_draw_discard(self):
        deck = Deck()
        card = deck.draw()
        assert len(deck) == DECK_SIZE - 1
        deck.discard(card)
        assert len(deck) == DECK_SIZE
        assert deck[card.id] is card
        with pytest.raises(ValueError):
            deck.discard(card)  # can't add it a 2nd time


# Unit tests for Pawn
class TestPawn:
    def test_constructor(self):
        pawn = Pawn("color", 0)
        assert pawn.color == "color"
        assert pawn.index == 0
        assert pawn.name == "color-0"
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_repr(self):
        Pawn("color", 0).__repr__()  # just make sure it doesn't blow up

    def test_move_to_start(self):
        pawn = Pawn("color", 0)
        pawn.start = "x"
        pawn.home = "x"
        pawn.safe = "x"
        pawn.square = "x"
        pawn.move_to_start()
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_home(self):
        pawn = Pawn("color", 0)
        pawn.start = "x"
        pawn.home = "x"
        pawn.safe = "x"
        pawn.square = "x"
        pawn.move_to_home()
        assert pawn.start is False
        assert pawn.home is True
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_safe_valid(self):
        for square in range(SAFE_SQUARES):
            pawn = Pawn("color", 0)
            pawn.start = "x"
            pawn.home = "x"
            pawn.safe = "x"
            pawn.square = "x"
            pawn.move_to_safe(square)
            assert pawn.start is False
            assert pawn.home is False
            assert pawn.safe == square
            assert pawn.square is None

    def test_move_to_safe_invalid(self):
        for square in [-1000, -2 - 1, 5, 6, 1000]:
            with pytest.raises(ValueError):
                pawn = Pawn("color", 0)
                pawn.move_to_safe(square)

    def test_move_to_square_invalid(self):
        for square in [-1000, -2 - 1, 60, 61, 1000]:
            with pytest.raises(ValueError):
                pawn = Pawn("color", 0)
                pawn.move_to_square(square)


# Unit tests for Pawns
class TestPawns:
    def test_constructor(self):
        pawns = Pawns("color")
        assert pawns.color == "color"
        assert len(pawns) == 4
        assert pawns[0].name == "color-0"
        assert pawns[1].name == "color-1"
        assert pawns[2].name == "color-2"
        assert pawns[3].name == "color-3"

    def test_repr(self):
        Pawns("color").__repr__()  # just make sure it doesn't blow up


# Unit tests for Player
class TestPlayer:
    def test_constructor_no_hand(self):
        player = Player("color")
        assert player.color == "color"
        assert player.name is None
        assert player.pawns is not None
        assert len(player.hand) == 0

    def test_constructor_with_hand(self):
        cards = [Card(0, "1"), Card(1, "12")]
        player = Player("color", cards=cards)
        assert player.color == "color"
        assert player.name is None
        assert player.pawns is not None
        assert len(player.hand) == len(cards)

    def test_repr(self):
        Player("color").__repr__()  # just make sure it doesn't blow up


# Unit tests for Players
class TestPlayers:
    def test_constructor_2_players(self):
        players = Players(2)
        assert len(players) == 2
        assert players[RED].color == RED
        assert players[YELLOW].color == YELLOW

    def test_constructor_3_players(self):
        players = Players(3)
        assert len(players) == 3
        assert players[RED].color == RED
        assert players[YELLOW].color == YELLOW
        assert players[GREEN].color == GREEN

    def test_constructor_4_players(self):
        players = Players(4)
        assert len(players) == 4
        assert players[RED].color == RED
        assert players[YELLOW].color == YELLOW
        assert players[GREEN].color == GREEN
        assert players[BLUE].color == BLUE

    def test_constructor_invalid_players(self):
        for p in [-2, -1, 0, 1, 5, 6]:
            with pytest.raises(ValueError):
                Players(p)

    def test_repr(self):
        Players(2).__repr__()  # just make sure it doesn't blow up
        Players(3).__repr__()  # just make sure it doesn't blow up
        Players(4).__repr__()  # just make sure it doesn't blow up

    def test_iterator(self):
        i = Players(4).__iter__()
        assert i.__next__().color == RED
        assert i.__next__().color == YELLOW
        assert i.__next__().color == GREEN
        assert i.__next__().color == BLUE
        with pytest.raises(StopIteration):
            i.__next__()


# Unit tests for Game
class TestGame:
    def test_constructor_valid_players(self):
        for p in [2, 3, 4]:
            game = Game(p)
            assert len(game.players) == p
            assert len(game.deck) == DECK_SIZE

    def test_constructor_invalid_players(self):
        for p in [-2, -1, 0, 1, 5, 6]:
            with pytest.raises(ValueError):
                Game(p)

    def test_repr(self):
        for p in [2, 3, 4]:
            Game(p).__repr__()  # just make sure it doesn't blow up
