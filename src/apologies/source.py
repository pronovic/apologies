# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Character input sources.  A character could be a person or could be computer-driven.
"""

import random
from abc import ABC, abstractmethod
from pydoc import locate
from typing import Callable, List

import attr

from .game import GameMode, PlayerView
from .rules import Move


class CharacterInputSource(ABC):

    """
    A generic source of input for a character, which could be a person or could be computer-driven.
    Concrete character input sources must have a valid zero-arguments constructor.
    """

    @abstractmethod
    def choose_move(
        self, mode: GameMode, view: PlayerView, legal_moves: List[Move], evaluator: Callable[[PlayerView, Move], PlayerView]
    ) -> Move:
        """
        Choose the next move for a character.

        There is always at least one legal move: a forfeit.  Nothing else is legal, so the
        character must choose to discard one card.  In standard mode, there is effectively no
        choice (since there is only one card in play), but in adult mode the character can choose
        which to discard.  If a move has an empty list of actions, then this is a forfeit.

        The source `must` return a move from among the passed-in set of legal moves.  If a source
        returns an illegal move, then a legal move will be chosen at random and executed.  This way,
        a misbehaving source (or a source attempting to cheat) does not get an advantage.  The game
        rules require a player to make a legal move if one is available, even if that move is
        disadvantageous.

        Args:
            mode(GameMode): Game mode
            view(PlayerView): Player-specific view of the game
            legal_moves(List[Move]): The set of legal moves
            evaluator(Callable[[PlayerView, Move], PlayerView]): Function to evaluate a move, returning new state

        Returns:
            Move: The character's next move as described above
        """


@attr.s
class RandomInputSource(CharacterInputSource):

    """
    A source of input for a character which chooses randomly from among legal moves.
    """

    def choose_move(
        self, mode: GameMode, view: PlayerView, legal_moves: List[Move], unused: Callable[[PlayerView, Move], PlayerView]
    ) -> Move:
        """Randomly choose the next move for a character."""
        return random.choice(legal_moves)


def source(name: str) -> CharacterInputSource:
    """
    Create a character input source by name.

    Args:
        name(str): Fully-qualified name of the source, like "apologies.source.RandomInputSource"

    Returns:
        CharacterInputSource: An instance of the named source

    Raises:
        ValueError: If the named source does not exist or is not a CharacterInputSource
    """
    cls = locate(name)
    if not issubclass(cls, CharacterInputSource):  # type: ignore
        raise ValueError("%s is not a CharacterInputSource" % name)
    return cls()  # type: ignore
