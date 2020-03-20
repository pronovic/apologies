# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Game engine that coordinates character actions to play a game.
"""

from typing import List, Dict
import attr
from .game import Game, GameMode, Player, PlayerColor, CardType
from .character import Character
from .util import CircularQueue

# For an adult-mode game, we deal out 5 cards
ADULT_HAND = 5

# The start squares for each color
_START_SQUARE = {
    PlayerColor.RED: 4,
    PlayerColor.BLUE: 19,
    PlayerColor.YELLOW: 34,
    PlayerColor.GREEN: 49,
}

# Whether a card draws again
_DRAW_AGAIN = {
    CardType.CARD_1: False,
    CardType.CARD_2: True,
    CardType.CARD_3: False,
    CardType.CARD_4: False,
    CardType.CARD_5: False,
    CardType.CARD_7: False,
    CardType.CARD_8: False,
    CardType.CARD_10: False,
    CardType.CARD_11: False,
    CardType.CARD_12: False,
    CardType.CARD_APOLOGIES: False,
}


@attr.s
class _Player:
    """Internal data for a character."""

    player = attr.ib(type=Player)
    character = attr.ib(type=Character)
    winner = attr.ib(init=False, default=False)


@attr.s
class Engine:

    """
    Game engine that coordinates character actions in a game.

    Attributes:
        mode(GameMode): The game mode
        characters(:obj: list of :obj: Character): Characters playing the game
        started(boolean): Whether the game is started
        completed(boolean): Whether the game is completed
        game(Game): The current state of the game, not to be modified by callers
        _players(:obj: list of :obj: _Player): Internal list of players
        _queue(CircularQueue): Queue that controls the order in which characters play
    """

    characters = attr.ib(type=List[Character])
    mode = attr.ib(default=GameMode.STANDARD, type=GameMode)
    started = attr.ib(init=False, default=False, type=bool)
    completed = attr.ib(init=False, default=False, type=bool)
    _game = attr.ib(init=False, type=Game)
    _queue = attr.ib(init=False, type=CircularQueue[PlayerColor])
    _players = attr.ib(init=False, type=Dict[PlayerColor, _Player])

    @_game.default
    def _init_game(self) -> Game:
        return Game(playercount=len(self.characters))

    @_queue.default
    def _init_queue(self) -> CircularQueue[PlayerColor]:
        return CircularQueue(list(PlayerColor)[: len(self.characters)])

    @_players.default
    def _init_players(self) -> Dict[PlayerColor, _Player]:
        index = 0
        players = {}
        for player in self._game.players.values():
            players[player.color] = _Player(player, self.characters[index])
            index += 1
        return players

    def start_game(self) -> Game:
        """Start the game, returning a copy of the current game state."""
        self.started = True
        if self.mode == GameMode.ADULT:
            self._setup_adult_mode()
        return self._game.copy()

    def _setup_adult_mode(self) -> None:
        """Setup adult mode at the start of the game, which moves some pieces and deals some cards."""
        for player in self._game.players.values():
            player.pawns[0].move_to_square(_START_SQUARE[player.color])
        for _ in range(ADULT_HAND):
            for player in self._game.players.values():
                player.hand.append(self._game.deck.draw())
