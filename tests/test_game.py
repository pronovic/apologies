# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access

import pytest
from flexmock import flexmock
from pendulum.datetime import DateTime

from apologies.game import (
    DECK_COUNTS,
    DECK_SIZE,
    PAWNS,
    SAFE_SQUARES,
    Card,
    CardType,
    Deck,
    Game,
    History,
    Pawn,
    Player,
    PlayerColor,
)


class TestCard:
    def test_constructor(self):
        card = Card(0, CardType.CARD_12)
        assert card.id == 0
        assert card.cardtype == CardType.CARD_12


class TestDeck:
    def test_constructor(self):
        deck = Deck()

        assert len(deck._draw_pile.keys()) == DECK_SIZE
        assert len(deck._discard_pile.keys()) == 0

        cardcounts = {cardtype: 0 for cardtype in CardType}
        for card in deck._draw_pile.values():
            cardcounts[card.cardtype] += 1
        for cardtype in CardType:
            assert cardcounts[cardtype] == DECK_COUNTS[cardtype]

    def test_draw_and_discard(self):
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
    def test_constructor(self):
        pawn = Pawn(PlayerColor.RED, 0)
        assert pawn.color == PlayerColor.RED
        assert pawn.index == 0
        assert pawn.name == "Red-0"
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_constructor_with_name(self):
        pawn = Pawn(PlayerColor.RED, 0, name="whatever")
        assert pawn.color == PlayerColor.RED
        assert pawn.index == 0
        assert pawn.name == "whatever"
        assert pawn.start is True
        assert pawn.home is False
        assert pawn.safe is None
        assert pawn.square is None

    def test_move_to_start(self):
        pawn = Pawn(PlayerColor.RED, 0)
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
        pawn = Pawn(PlayerColor.RED, 0)
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
            pawn = Pawn(PlayerColor.RED, 0)
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
                pawn = Pawn(PlayerColor.RED, 0)
                pawn.move_to_safe(square)

    def test_move_to_square_invalid(self):
        for square in [-1000, -2 - 1, 60, 61, 1000]:
            with pytest.raises(ValueError):
                pawn = Pawn(PlayerColor.RED, 0)
                pawn.move_to_square(square)


class TestPlayer:
    def test_constructor(self):
        player = Player(PlayerColor.RED)
        assert player.color == PlayerColor.RED
        assert len(player.pawns) == PAWNS
        for pawn in player.pawns:
            assert isinstance(pawn, Pawn)

    def test_find_first_pawn_in_start(self):
        player = Player(PlayerColor.RED)
        for i in range(PAWNS):
            assert player.find_first_pawn_in_start() is player.pawns[i]
            player.pawns[i].move_to_home()
        assert player.find_first_pawn_in_start() is None

    def test_all_pawns_in_home(self):
        player = Player(PlayerColor.RED)
        for i in range(PAWNS):
            assert player.all_pawns_in_home() is False
            player.pawns[i].move_to_home()
        assert player.all_pawns_in_home() is True


class TestHistory:
    def test_constructor(self):
        color = PlayerColor.BLUE
        history = History("action", color)
        assert history.color is color
        assert history.action == "action"
        assert history.timestamp <= DateTime.utcnow()


class TestGame:
    def test_constructor_2_players_standard(self):
        game = Game(2)
        assert len(game.players) == 2
        assert len(game.history) == 0
        for color in [PlayerColor.RED, PlayerColor.YELLOW]:
            assert game.players[color].color == color
            assert len(game.players[color].hand) == 0
        assert game.deck is not None

    def test_constructor_3_players_standard(self):
        game = Game(3)
        assert len(game.players) == 3
        assert len(game.history) == 0
        for color in [PlayerColor.RED, PlayerColor.YELLOW, PlayerColor.GREEN]:
            assert game.players[color].color == color
            assert len(game.players[color].hand) == 0
        assert game.deck is not None

    def test_constructor_4_players_standard(self):
        game = Game(4)
        assert len(game.players) == 4
        assert len(game.history) == 0
        for color in [PlayerColor.RED, PlayerColor.YELLOW, PlayerColor.GREEN, PlayerColor.BLUE]:
            assert game.players[color].color == color
            assert len(game.players[color].hand) == 0
        assert game.deck is not None

    def test_constructor_invalid_players(self):
        for playercount in [-2, -1, 0, 1, 5, 6]:
            with pytest.raises(ValueError):
                Game(playercount)

    def test_copy(self):
        game = Game(4)
        game.track("this happened", game.players[PlayerColor.RED])
        game.players[PlayerColor.RED].pawns[0].move_to_square(32)
        game.players[PlayerColor.BLUE].pawns[2].move_to_home()
        game.players[PlayerColor.YELLOW].pawns[3].move_to_safe(1)
        game.players[PlayerColor.GREEN].pawns[1].move_to_square(19)
        copy = game.copy()
        assert copy == game

    def test_json_roundtrip(self):
        game = Game(4)
        game.track("this happened", game.players[PlayerColor.RED])
        game.players[PlayerColor.RED].pawns[0].move_to_square(32)
        game.players[PlayerColor.BLUE].pawns[2].move_to_home()
        game.players[PlayerColor.YELLOW].pawns[3].move_to_safe(1)
        game.players[PlayerColor.GREEN].pawns[1].move_to_square(19)
        data = game.to_json()
        copy = Game.from_json(data)
        assert copy == game

    def test_track_no_player(self):
        game = Game(4)
        game.track("action")
        assert game.history == [History("action")]

    def test_track_with_player(self):
        game = Game(4)
        player = flexmock(color=PlayerColor.RED)
        game.track("action", player)
        assert game.history == [History("action", PlayerColor.RED)]

    def test_find_pawn_on_square(self):
        game = Game(4)
        assert game.find_pawn_on_square(32) is None
        game.players[PlayerColor.RED].pawns[0].move_to_square(32)
        assert game.find_pawn_on_square(32) is game.players[PlayerColor.RED].pawns[0]
        game.players[PlayerColor.GREEN].pawns[0].move_to_square(32)
        assert game.find_pawn_on_square(32) is game.players[PlayerColor.RED].pawns[0]  # returns the first found

    def test_started(self):
        game = Game(4)
        assert game.started is False
        game.track("whatever")
        assert game.started is True

    def test_completed(self):
        game = Game(4)

        # move all but last pawn into home for all of the players; the game is not complete
        for player in game.players.values():
            for i in range(PAWNS - 1):
                assert game.completed is False
                player.pawns[i].move_to_home()

        # move the final pawn to home for one player; now the game is complete
        game.players[PlayerColor.RED].pawns[PAWNS - 1].move_to_home()
        assert game.completed is True
