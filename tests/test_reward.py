# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

from apologies.game import Game, PlayerColor
from apologies.reward import RewardCalculatorV1


class TestRewardCalculatorV1:
    """
    Unit tests for RewardCalculatorV1.
    """

    def test_range(self):
        assert RewardCalculatorV1().range(2) == (0, 400)
        assert RewardCalculatorV1().range(3) == (0, 800)
        assert RewardCalculatorV1().range(4) == (0, 1200)

    def test_empty_game(self):
        for playercount in [2, 3, 4]:
            for color in list(PlayerColor)[:playercount]:
                game = Game(playercount=playercount)
                view = game.create_player_view(color)
                assert RewardCalculatorV1().calculate(view) == 0  # score is always zero if all pawns are in start

    def test_equivalent_state(self):
        game = Game(playercount=4)
        game.players[PlayerColor.RED].pawns[0].position.move_to_square(4)
        game.players[PlayerColor.YELLOW].pawns[0].position.move_to_square(34)
        game.players[PlayerColor.GREEN].pawns[0].position.move_to_square(49)
        game.players[PlayerColor.BLUE].pawns[0].position.move_to_square(19)
        for color in PlayerColor:
            view = game.create_player_view(color)
            assert RewardCalculatorV1().calculate(view) == 0  # score is always zero if all players are equivalent

    def test_safe_zone(self):
        game = Game(playercount=4)
        game.players[PlayerColor.RED].pawns[0].position.move_to_safe(4)  # last safe square before home
        view = game.create_player_view(PlayerColor.RED)
        assert RewardCalculatorV1().calculate(view) == 222
        for color in [PlayerColor.BLUE, PlayerColor.YELLOW, PlayerColor.GREEN]:
            view = game.create_player_view(color)
            assert RewardCalculatorV1().calculate(view) == 0  # score is always zero if all pawns are in start

    def test_winner(self):
        game = Game(playercount=2)
        game.players[PlayerColor.RED].pawns[0].position.move_to_home()
        game.players[PlayerColor.RED].pawns[1].position.move_to_home()
        game.players[PlayerColor.RED].pawns[2].position.move_to_home()
        game.players[PlayerColor.RED].pawns[3].position.move_to_home()
        view = game.create_player_view(PlayerColor.RED)
        assert RewardCalculatorV1().calculate(view) == 400
        for color in [PlayerColor.YELLOW]:
            view = game.create_player_view(color)
            assert RewardCalculatorV1().calculate(view) == 0  # score is always zero if all pawns are in start

        game = Game(playercount=3)
        game.players[PlayerColor.RED].pawns[0].position.move_to_home()
        game.players[PlayerColor.RED].pawns[1].position.move_to_home()
        game.players[PlayerColor.RED].pawns[2].position.move_to_home()
        game.players[PlayerColor.RED].pawns[3].position.move_to_home()
        view = game.create_player_view(PlayerColor.RED)
        assert RewardCalculatorV1().calculate(view) == 800
        for color in [PlayerColor.YELLOW, PlayerColor.GREEN]:
            view = game.create_player_view(color)
            assert RewardCalculatorV1().calculate(view) == 0  # score is always zero if all pawns are in start

        game = Game(playercount=4)
        game.players[PlayerColor.RED].pawns[0].position.move_to_home()
        game.players[PlayerColor.RED].pawns[1].position.move_to_home()
        game.players[PlayerColor.RED].pawns[2].position.move_to_home()
        game.players[PlayerColor.RED].pawns[3].position.move_to_home()
        view = game.create_player_view(PlayerColor.RED)
        assert RewardCalculatorV1().calculate(view) == 1200
        for color in [PlayerColor.YELLOW, PlayerColor.GREEN, PlayerColor.BLUE]:
            view = game.create_player_view(color)
            assert RewardCalculatorV1().calculate(view) == 0  # score is always zero if all pawns are in start

    def test_arbitrary(self):
        game = Game(playercount=4)

        game.players[PlayerColor.RED].pawns[0].position.move_to_home()
        game.players[PlayerColor.RED].pawns[1].position.move_to_safe(0)
        game.players[PlayerColor.RED].pawns[2].position.move_to_square(6)
        game.players[PlayerColor.RED].pawns[3].position.move_to_square(10)

        game.players[PlayerColor.YELLOW].pawns[0].position.move_to_square(34)
        game.players[PlayerColor.YELLOW].pawns[1].position.move_to_square(32)
        game.players[PlayerColor.YELLOW].pawns[2].position.move_to_start()
        game.players[PlayerColor.YELLOW].pawns[3].position.move_to_home()

        game.players[PlayerColor.GREEN].pawns[0].position.move_to_start()
        game.players[PlayerColor.GREEN].pawns[1].position.move_to_start()
        game.players[PlayerColor.GREEN].pawns[2].position.move_to_square(59)
        game.players[PlayerColor.GREEN].pawns[3].position.move_to_start()

        game.players[PlayerColor.BLUE].pawns[0].position.move_to_start()
        game.players[PlayerColor.BLUE].pawns[1].position.move_to_start()
        game.players[PlayerColor.BLUE].pawns[2].position.move_to_start()
        game.players[PlayerColor.BLUE].pawns[3].position.move_to_start()

        view = game.create_player_view(PlayerColor.RED)
        assert RewardCalculatorV1().calculate(view) == 319

        view = game.create_player_view(PlayerColor.YELLOW)
        assert RewardCalculatorV1().calculate(view) == 239

        view = game.create_player_view(PlayerColor.GREEN)
        assert RewardCalculatorV1().calculate(view) == 0

        view = game.create_player_view(PlayerColor.BLUE)
        assert RewardCalculatorV1().calculate(view) == 0
