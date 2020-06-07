# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=no-self-use,protected-access

from unittest.mock import MagicMock

import pendulum
import pytest
from pendulum.datetime import DateTime

from apologies.game import (
    BOARD_SQUARES,
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
    PlayerView,
    Position,
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

        # Check that we can draw the entire deck
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

        # Confirm that we're not allowed to discard the same card twice
        card = drawn.pop()
        deck.discard(card)
        with pytest.raises(ValueError):
            deck.discard(card)

        # Discard a few others and prove they can also be drawn
        deck.discard(drawn.pop())
        deck.discard(drawn.pop())
        deck.discard(drawn.pop())
        assert len(deck._discard_pile) == 4
        assert len(deck._draw_pile) == 0
        deck.draw()
        assert len(deck._discard_pile) == 0
        assert len(deck._draw_pile) == 3
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
class TestPosition:
    def test_constructor(self):
        position = Position()
        assert position.start is True
        assert position.home is False
        assert position.safe is None
        assert position.square is None
        assert "%s" % position == "start"

    def test_copy(self):
        position = Position()
        assert position.start is True
        assert position.home is False
        position.safe = 9
        position.square = 13
        copy = position.copy()
        assert copy is not position and copy == position

    def test_move_to_position_valid_start(self):
        target = Position()
        target.start = True
        target.home = False
        target.safe = None
        target.square = None
        position = Position()
        position.start = "x"
        position.home = "x"
        position.safe = "x"
        position.square = "x"
        result = position.move_to_position(target)
        assert result is position
        assert position == target
        assert "%s" % position == "start"

    def test_move_to_position_valid_home(self):
        target = Position()
        target.start = False
        target.home = True
        target.safe = None
        target.square = None
        position = Position()
        position.start = "x"
        position.home = "x"
        position.safe = "x"
        position.square = "x"
        result = position.move_to_position(target)
        assert result is position
        assert position == target
        assert "%s" % position == "home"

    def test_move_to_position_valid_safe(self):
        target = Position()
        target.start = False
        target.home = False
        target.safe = 3
        target.square = None
        position = Position()
        position.start = "x"
        position.home = "x"
        position.safe = "x"
        position.square = "x"
        result = position.move_to_position(target)
        assert result is position
        assert position == target
        assert "%s" % position == "safe 3"

    def test_move_to_position_valid_square(self):
        target = Position()
        target.start = False
        target.home = False
        target.safe = None
        target.square = 3
        position = Position()
        position.start = "x"
        position.home = "x"
        position.safe = "x"
        position.square = "x"
        result = position.move_to_position(target)
        assert result is position
        assert position == target
        assert "%s" % position == "square 3"

    def test_move_to_position_invalid_multiple(self):
        position = Position()
        for (start, home, safe, square) in [
            (True, True, None, None),
            (True, False, 1, None),
            (True, False, None, 1),
            (False, True, 1, None),
            (False, True, None, 1),
            (False, False, 1, 1),
        ]:
            with pytest.raises(ValueError):
                target = Position()
                target.start = start
                target.home = home
                target.safe = safe
                target.square = square
                position.move_to_position(target)

    def test_move_to_position_invalid_none(self):
        position = Position()
        with pytest.raises(ValueError):
            target = Position()
            target.start = False
            target.home = False
            target.safe = None
            target.square = None
            position.move_to_position(target)

    def test_move_to_position_invalid_safe(self):
        position = Position()
        for square in [-1000, -2 - 1, 5, 6, 1000]:
            with pytest.raises(ValueError):
                target = Position()
                target.safe = square
                position.move_to_position(target)

    def test_move_to_position_invalid_square(self):
        position = Position()
        for square in [-1000, -2 - 1, 60, 61, 1000]:
            with pytest.raises(ValueError):
                target = Position()
                target.square = square
                position.move_to_position(target)

    def test_move_to_start(self):
        position = Position()
        position.start = "x"
        position.home = "x"
        position.safe = "x"
        position.square = "x"
        result = position.move_to_start()
        assert result is position
        assert position.start is True
        assert position.home is False
        assert position.safe is None
        assert position.square is None
        assert "%s" % position == "start"

    def test_move_to_home(self):
        position = Position()
        position.start = "x"
        position.home = "x"
        position.safe = "x"
        position.square = "x"
        result = position.move_to_home()
        assert result is position
        assert position.start is False
        assert position.home is True
        assert position.safe is None
        assert position.square is None
        assert "%s" % position == "home"

    def test_move_to_safe_valid(self):
        for square in range(SAFE_SQUARES):
            position = Position()
            position.start = "x"
            position.home = "x"
            position.safe = "x"
            position.square = "x"
            result = position.move_to_safe(square)
            assert result is position
            assert position.start is False
            assert position.home is False
            assert position.safe == square
            assert position.square is None
            assert "%s" % position == "safe %d" % square

    def test_move_to_safe_invalid(self):
        for square in [-1000, -2 - 1, 5, 6, 1000]:
            with pytest.raises(ValueError):
                position = Position()
                position.move_to_safe(square)

    def test_move_to_square_valid(self):
        for square in range(BOARD_SQUARES):
            position = Position()
            position.start = "x"
            position.home = "x"
            position.safe = "x"
            position.square = "x"
            result = position.move_to_square(square)
            assert result is position
            assert position.start is False
            assert position.home is False
            assert position.safe is None
            assert position.square is square
            assert "%s" % position == "square %d" % square

    def test_move_to_square_invalid(self):
        for square in [-1000, -2 - 1, 60, 61, 1000]:
            with pytest.raises(ValueError):
                position = Position()
                position.move_to_square(square)


class TestPawn:
    def test_constructor(self):
        pawn = Pawn(PlayerColor.RED, 0)
        assert pawn.color == PlayerColor.RED
        assert pawn.index == 0
        assert pawn.name == "Red0"
        assert pawn.position == Position()
        assert "%s" % pawn == "Red0->start"  # because default position is in start

    def test_constructor_with_name(self):
        pawn = Pawn(PlayerColor.RED, 0, name="whatever")
        assert pawn.color == PlayerColor.RED
        assert pawn.index == 0
        assert pawn.name == "whatever"
        assert pawn.position == Position()
        assert "%s" % pawn == "whatever->start"  # because default position is in start


class TestPlayer:
    def test_constructor(self):
        player = Player(PlayerColor.RED)
        assert player.color == PlayerColor.RED
        assert player.turns == 0
        assert len(player.pawns) == PAWNS
        for pawn in player.pawns:
            assert isinstance(pawn, Pawn)

    def test_copy(self):
        player = Player(PlayerColor.RED)
        player.pawns[0].position.move_to_home()
        player.pawns[1].position.move_to_safe(2)
        player.pawns[2].position.move_to_square(32)
        copy = player.copy()
        assert copy is not player and copy == player

    def test_find_first_pawn_in_start(self):
        player = Player(PlayerColor.RED)
        for i in range(PAWNS):
            assert player.find_first_pawn_in_start() is player.pawns[i]
            player.pawns[i].position.move_to_home()
        assert player.find_first_pawn_in_start() is None

    def test_all_pawns_in_home(self):
        player = Player(PlayerColor.RED)
        for i in range(PAWNS):
            assert player.all_pawns_in_home() is False
            player.pawns[i].position.move_to_home()
        assert player.all_pawns_in_home() is True


class TestHistory:
    def test_constructor(self):
        color = PlayerColor.BLUE
        card = CardType.CARD_APOLOGIES
        history = History("action", color, card)
        assert history.action == "action"
        assert history.color is color
        assert history.card is card
        assert history.timestamp <= DateTime.utcnow()

    def test_str(self):
        timestamp = pendulum.parse("2020-03-25T14:02:16")

        history = History("This is an action", color=None, timestamp=timestamp)
        assert "%s" % history == "[14:02:16] General - This is an action"

        history = History("This is an action", color=PlayerColor.BLUE, timestamp=timestamp)
        assert "%s" % history == "[14:02:16] Blue - This is an action"

        history = History("This is an action", color=PlayerColor.BLUE, card=CardType.CARD_10, timestamp=timestamp)
        assert "%s" % history == "[14:02:16] Blue - This is an action"


class TestPlayerView:
    def test_constructor(self):
        player = Player(PlayerColor.RED)
        opponents = {PlayerColor.GREEN: Player(PlayerColor.GREEN)}
        view = PlayerView(player, opponents)
        assert view.player == player
        assert view.opponents == opponents

    def test_copy(self):
        player = Player(PlayerColor.RED)
        opponents = {PlayerColor.GREEN: Player(PlayerColor.GREEN)}
        view = PlayerView(player, opponents)
        copy = view.copy()
        assert copy is not view and copy == view

    def test_get_pawn(self):
        player = Player(PlayerColor.RED)
        opponents = {PlayerColor.GREEN: Player(PlayerColor.GREEN)}
        view = PlayerView(player, opponents)
        assert view.get_pawn(MagicMock(color=PlayerColor.RED, index=3)) == view.player.pawns[3]
        assert view.get_pawn(MagicMock(color=PlayerColor.GREEN, index=1)) == view.opponents[PlayerColor.GREEN].pawns[1]
        assert view.get_pawn(MagicMock(color=PlayerColor.YELLOW, index=0)) is None

    def test_all_pawns(self):
        player = Player(PlayerColor.RED)
        opponents = {PlayerColor.GREEN: Player(PlayerColor.GREEN)}
        view = PlayerView(player, opponents)
        pawns = view.all_pawns()
        assert len(pawns) == 2 * PAWNS
        for i in range(PAWNS):
            assert player.pawns[i] in pawns
            assert opponents[PlayerColor.GREEN].pawns[i] in pawns


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

    def test_started(self):
        game = Game(4)
        assert game.started is False
        game.track("whatever")
        assert game.started is True

    def test_completed_and_winner(self):
        game = Game(4)

        # move all but last pawn into home for all of the players; the game is not complete
        for player in game.players.values():
            for i in range(PAWNS - 1):
                assert game.completed is False
                player.pawns[i].position.move_to_home()

        # move the final pawn to home for one player; now the game is complete
        game.players[PlayerColor.RED].pawns[PAWNS - 1].position.move_to_home()

        assert game.completed is True
        assert game.winner is game.players[PlayerColor.RED]

    def test_copy(self):
        game = TestGame._create_realistic_game()
        copy = game.copy()
        assert copy == game

    def test_json_roundtrip(self):
        game = TestGame._create_realistic_game()
        data = game.to_json()
        copy = Game.from_json(data)
        assert copy == game

    def test_track_no_player(self):
        game = Game(4)
        game.track("action")
        assert game.history[0].action == "action"
        assert game.history[0].color is None
        assert game.history[0].card is None
        assert game.history[0].timestamp <= DateTime.utcnow()
        assert game.players[PlayerColor.RED].turns == 0
        assert game.players[PlayerColor.YELLOW].turns == 0
        assert game.players[PlayerColor.BLUE].turns == 0
        assert game.players[PlayerColor.GREEN].turns == 0

    def test_track_with_color(self):
        game = Game(4)
        player = MagicMock(color=PlayerColor.RED)
        card = MagicMock(cardtype=CardType.CARD_12)
        game.track("action", player, card)
        assert game.history[0].action == "action"
        assert game.history[0].color is PlayerColor.RED
        assert game.history[0].card == CardType.CARD_12
        assert game.history[0].timestamp <= DateTime.utcnow()
        assert game.players[PlayerColor.RED].turns == 1
        assert game.players[PlayerColor.YELLOW].turns == 0
        assert game.players[PlayerColor.BLUE].turns == 0
        assert game.players[PlayerColor.GREEN].turns == 0

    def test_create_player_view_invalid(self):
        game = Game(2)
        with pytest.raises(KeyError):
            game.create_player_view(PlayerColor.BLUE)  # no blue player in 2-player game

    def test_create_player_view(self):
        game = Game(4)

        game.players[PlayerColor.RED].hand.append(game.deck.draw())
        game.players[PlayerColor.YELLOW].hand.append(game.deck.draw())
        game.players[PlayerColor.GREEN].hand.append(game.deck.draw())
        game.players[PlayerColor.BLUE].hand.append(game.deck.draw())

        view = game.create_player_view(PlayerColor.RED)

        assert game.players[PlayerColor.RED] is not view.player
        assert game.players[PlayerColor.YELLOW] is not view.opponents[PlayerColor.YELLOW]

        assert game.players[PlayerColor.RED] == view.player

        for color in [PlayerColor.YELLOW, PlayerColor.GREEN, PlayerColor.BLUE]:
            assert view.opponents[color].color == color
            assert len(view.opponents[color].hand) == 0
            assert view.opponents[color].pawns == game.players[color].pawns

    @staticmethod
    def _create_realistic_game():
        """Create a realistic game with changes to the defaults for all types of values."""
        game = Game(4)
        game.track("this happened")
        game.track("another thing", game.players[PlayerColor.RED])
        card1 = game.deck.draw()
        card2 = game.deck.draw()
        game.deck.draw()  # just throw it away
        game.deck.discard(card1)
        game.deck.discard(card2)
        game.players[PlayerColor.RED].pawns[0].position.move_to_square(32)
        game.players[PlayerColor.BLUE].pawns[2].position.move_to_home()
        game.players[PlayerColor.BLUE].hand.append(card1)
        game.players[PlayerColor.YELLOW].pawns[3].position.move_to_safe(1)
        game.players[PlayerColor.GREEN].pawns[1].position.move_to_square(19)
        game.players[PlayerColor.GREEN].hand.append(card2)
        return game
