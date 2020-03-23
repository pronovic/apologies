# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Game engine that coordinates character actions to play a game.
"""


from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import attr

from .game import Card, Game, GameMode, PlayerColor, PlayerView
from .rules import Move, Rules, ValidationError
from .util import CircularQueue


class CharacterInputSource(ABC):

    """A generic source of input for a character, which could be a person or could be computer-driven."""

    @abstractmethod
    def construct_move(
        self, mode: GameMode, view: PlayerView, card: Optional[Card] = None, invalid: Optional[bool] = False
    ) -> Move:
        """
        Construct the next move for a character.

        The passed-in game, player, and card must not be modified.

        If no move is possible, then return an empty list of actions.  If a card was passed-in, always
        attach it to the returned Move.  Otherwise, attach the card that is being played.  The attached
        card is always discarded back to the deck.

        Args:
            mode(GameMode): Game mode
            view(PlayerView): Player-specific view of the game
            card(Card, optional): The card to play, or None if move should come from player's hand
            invalid(bool, optional): Whether this call is because a previous move was invalid

        Returns:
            Move: the character's next move, an empty list if no move is possible and the turn is forfeit
        """


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

    def construct_move(
        self, mode: GameMode, view: PlayerView, card: Optional[Card] = None, invalid: Optional[bool] = False
    ) -> Move:
        """
        Construct the next move for a character via the user input source.

        Args:
            mode(GameMode): Game mode
            view(PlayerView): Player-specific view of the game
            card(Card, optional): The card to play, or None if move should come from player's hand
            invalid(bool, optional): Whether this call is because a previous move was invalid

        Returns:
            Move: the character's next move, an empty list if no move is possible and the turn is forfeit
        """
        return self.source.construct_move(mode, view, card, invalid)


@attr.s
class Engine:

    """
    Game engine that coordinates character actions in a game.

    Attributes:
        mode(GameMode): The game mode
        characters(:obj: list of :obj: Character): Characters playing the game
        started(boolean): Whether the game is started
        completed(boolean): Whether the game is completed
        _game(Game): The current state of the game, not to be modified by callers
        _queue(CircularQueue): Queue that controls the order in which characters play
        _rules(Rules): Implements all rules related to game play
    """

    mode = attr.ib(type=GameMode)
    characters = attr.ib(type=List[Character])
    _game = attr.ib(init=False, type=Game)
    _queue = attr.ib(init=False, type=CircularQueue[PlayerColor])
    _rules = attr.ib(init=False, type=Rules)
    _map = attr.ib(init=False, type=Dict[PlayerColor, Character])

    @_game.default
    def _init_game(self) -> Game:
        return Game(playercount=len(self.characters))

    @_queue.default
    def _init_queue(self) -> CircularQueue[PlayerColor]:
        return CircularQueue(list(PlayerColor)[: len(self.characters)])

    @_rules.default
    def _init_rules(self) -> Rules:
        return Rules(self.mode)

    @_map.default
    def _init_map(self) -> Dict[PlayerColor, Character]:
        index = 0
        result = {}
        for player in self._game.players.values():
            result[player.color] = self.characters[index]
            index += 1
        return result

    @property
    def started(self) -> bool:
        """Whether the game is started."""
        return self._game.started

    @property
    def completed(self) -> bool:
        """Whether the game is completed."""
        return self._game.completed

    def start_game(self) -> Game:
        """
        Start the game, returning game state.

        Returns:
            Current state of the game.
        """
        self._rules.start_game(self._game)
        return self._game

    def play_next(self) -> Game:
        """
        Play the next move of the game, returning initial game state.

        Returns:
            Current state of the game.
        """
        if self.completed:
            raise ValueError("Game is complete")
        saved = self._game.copy()
        try:
            color = self._queue.next()
            if self.mode == GameMode.ADULT:
                self._play_next_adult(color)
            else:
                card = self._game.deck.draw()
                self._play_next_standard(color, card)
            return self._game
        except Exception as e:
            self._game = saved  # put back original so a failed call is idempotent
            raise e

    def _play_next_standard(self, color: PlayerColor, card: Card, invalid: Optional[bool] = False) -> None:
        """Play the next move under the rules for standard mode."""
        player = self._game.players[color]
        character = self._map[color]
        view = self._game.create_player_view(color)
        move = character.construct_move(self.mode, view, card=card, invalid=invalid)
        if not move.actions:
            self._game.track("Turn forfeited", player)
            self._game.deck.discard(card)
        else:
            if not self._validate_move(color, move):
                self._game.track("Requested move was invalid", player)
                self._play_next_standard(color, card, invalid=True)  # recursive call; try again with no change in state
            else:
                self._rules.execute_move(self._game, color, move)  # tracks history, potentially completes game
                self._game.deck.discard(card)
                if not self.completed and self._rules.draw_again(card):
                    card = self._game.deck.draw()
                    self._play_next_standard(color, card, invalid=False)  # recursive call for next move

    def _play_next_adult(self, color: PlayerColor, invalid: Optional[bool] = False) -> None:
        """Play the next move under the rules for adult mode."""
        player = self._game.players[color]
        character = self._map[color]
        view = self._game.create_player_view(color)
        move = character.construct_move(self.mode, view, card=None, invalid=invalid)
        if not move.actions:
            self._game.track("Turn forfeited", player)
            player.hand.remove(move.card)
            self._game.deck.discard(move.card)
            player.hand.append(self._game.deck.draw())
        else:
            if not self._validate_move(color, move):
                self._game.track("Requested move was invalid", player)
                self._play_next_adult(color, invalid=True)  # recursive call; try again with no change in state
            else:
                self._rules.execute_move(self._game, color, move)  # tracks history, potentially completes game
                player.hand.remove(move.card)
                self._game.deck.discard(move.card)
                player.hand.append(self._game.deck.draw())
                if not self.completed and self._rules.draw_again(move.card):
                    self._play_next_adult(color, invalid=False)  # recursive call for next move

    def _validate_move(self, color: PlayerColor, move: Move) -> bool:
        """Validate a player's move."""
        copy = self._game.copy()
        try:
            # We simply execute the move against a copy of the game.  If the
            # move is invalid, then an exception is thrown, but the state of
            # the original game is unchanged, so the caller is not impacted.
            self._rules.execute_move(copy, color, move)
            return True
        except ValidationError:
            return False
