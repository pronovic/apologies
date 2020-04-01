# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Game engine that coordinates character actions to play a game.
"""

import random
from typing import Callable, Dict, List

import attr

from .game import Game, GameMode, Player, PlayerColor, PlayerView
from .rules import Move, Rules
from .source import CharacterInputSource
from .util import CircularQueue


@attr.s
class Character:

    """
    A character that plays a game, which could be a person or could be computer-driven.

    Attributes:
        name(str): The name of this character
        source(CharacterInputSource): The character input source from which moves are taken
    """

    name = attr.ib(type=str)
    source = attr.ib(type=CharacterInputSource)

    def choose_move(
        self, mode: GameMode, view: PlayerView, legal_moves: List[Move], evaluator: Callable[[PlayerView, Move], PlayerView]
    ) -> Move:
        """
        Choose the next move for a character via the user input source.

        Args:
            mode(GameMode): Game mode
            view(PlayerView): Player-specific view of the game
            legal_moves(Set[Move]): The set of legal moves
            evaluator(Callable[[PlayerView, Move], PlayerView]): Function to evaluate a move, returning new state

        Returns:
            Move: The character's next as chosen by the configured source
        """
        return self.source.choose_move(mode, view, legal_moves, evaluator)


@attr.s
class Engine:

    """
    Game engine that coordinates character actions in a game.

    Normally, playing a game via an engine is as simple as::

        engine.start_game()
        while not engine.completed:
          state = engine.play_next()

    This plays a turn for each player, one after another, until the
    game is complete.  Other, more fine-grained methods exist if you
    need to structure game play differently for your purposes (for
    instance, to train a machine learning model).

    Attributes:
        mode(GameMode): The game mode
        characters(List[Character]): Characters playing the game
    """

    mode = attr.ib(type=GameMode)
    characters = attr.ib(type=List[Character])
    _game = attr.ib(init=False, type=Game)
    _queue = attr.ib(init=False, type=CircularQueue[PlayerColor])
    _rules = attr.ib(init=False, type=Rules)
    _map = attr.ib(init=False, type=Dict[PlayerColor, Character])

    @_game.default
    def _default_game(self) -> Game:
        return Game(playercount=len(self.characters))

    @_queue.default
    def _default_queue(self) -> CircularQueue[PlayerColor]:
        return CircularQueue(list(PlayerColor)[: len(self.characters)])

    @_rules.default
    def _default_rules(self) -> Rules:
        return Rules(self.mode)

    @_map.default
    def _default_map(self) -> Dict[PlayerColor, Character]:
        index = 0
        result = {}
        for player in self._game.players.values():
            result[player.color] = self.characters[index]
            index += 1
        return result

    @property
    def players(self) -> int:
        """Number of players in the game."""
        return len(self.characters)

    @property
    def state(self) -> str:
        """String describing the state of the game."""
        if self.completed:
            return "Game completed"
        elif self.started:
            return "Game in progress"
        else:
            return "Game waiting to start"

    @property
    def game(self) -> Game:
        """A reference to the underlying game."""
        return self._game

    @property
    def started(self) -> bool:
        """Whether the game is started."""
        return self._game.started

    @property
    def completed(self) -> bool:
        """Whether the game is completed."""
        return self._game.completed

    def reset(self) -> Game:
        """Reset game state."""
        self._game = self._default_game()
        return self._game

    def start_game(self) -> Game:
        """
        Start the game, returning game state.

        Returns:
            Game: Current state of the game.
        """
        self._rules.start_game(self._game)
        return self._game

    def play_next(self) -> Game:
        """
        Play the next turn of the game, returning initial game state.

        Returns:
            Game: Current state of the game.
        """
        if self.completed:
            raise ValueError("Game is complete")

        saved = self._game.copy()
        try:
            color = self._queue.next()
            character = self._map[color]

            done = False
            while not done:
                view = self._game.create_player_view(color)
                move = self.choose_next_move(character, view)
                done = self.execute_move(color, move)

            return self._game
        except Exception as e:
            self._game = saved  # put back original so a failed call is idempotent
            raise e

    def construct_legal_moves(self, view: PlayerView) -> List[Move]:
        """Construct the legal moves based on a player view."""
        return self._rules.construct_legal_moves(view, card=None if self.mode == GameMode.ADULT else self._game.deck.draw())

    def choose_next_move(self, character: Character, view: PlayerView) -> Move:
        """Choose the next move for a character based on a player view."""
        legal_moves = self.construct_legal_moves(view)
        move = character.choose_move(self.mode, view, legal_moves[:], Rules.evaluate_move)
        if move not in legal_moves:  # an illegal move is ignored and we choose randomly for the character
            self._game.track("Illegal move: a random legal move will be chosen", view.player)
            move = random.choice(legal_moves)
        return move

    def execute_move(self, color: PlayerColor, move: Move) -> bool:
        """Execute a move for a player, returning True if the player's turn is done."""
        player = self._game.players[color]
        if self.mode == GameMode.ADULT:
            return self._execute_move_adult(player, move)
        else:
            return self._execute_move_standard(player, move)

    def _execute_move_standard(self, player: Player, move: Move) -> bool:
        """Play the next turn under the rules for standard mode, returning True if the player's turn is done."""
        if not move.actions:
            self._game.deck.discard(move.card)
            self._game.track("Turn is forfeit; discarded card %s" % move.card.cardtype.value, player)
            return True  # player's turn is done if they forfeit
        else:
            self._rules.execute_move(self._game, player, move)  # tracks history, potentially completes game
            self._game.deck.discard(move.card)
            return self.completed or not self._rules.draw_again(move.card)  # player's turn is done unless they can draw again

    def _execute_move_adult(self, player: Player, move: Move) -> bool:
        """Play the next move under the rules for adult mode, returning True if the player's turn is done."""
        if not move.actions:
            player.hand.remove(move.card)
            self._game.deck.discard(move.card)
            player.hand.append(self._game.deck.draw())
            self._game.track("Turn is forfeit; discarded card %s" % move.card.cardtype.value, player)
            return True  # player's turn is done if they forfeit
        else:
            self._rules.execute_move(self._game, player, move)  # tracks history, potentially completes game
            player.hand.remove(move.card)
            self._game.deck.discard(move.card)
            player.hand.append(self._game.deck.draw())
            return self.completed or not self._rules.draw_again(move.card)  # player's turn is done unless they can draw again
