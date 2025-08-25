# vim: set ft=python ts=4 sw=4 expandtab:
# ruff: noqa: S311

"""
Character input sources.  A character could be a person or could be computer-driven.
"""

import operator
import random
from abc import ABC, abstractmethod
from collections.abc import Callable
from pydoc import locate

from apologies.game import GameMode, PlayerView
from apologies.reward import RewardCalculatorV1
from apologies.rules import Move


class CharacterInputSource(ABC):
    """
    A generic source of input for a character, which could be a person or could be computer-driven.
    Concrete character input sources must have a valid zero-arguments constructor.
    """

    @property
    def fullname(self) -> str:
        """Get the fully-qualified name of the character input source."""
        return f"{type(self).__module__}.{type(self).__name__}"

    @property
    def name(self) -> str:
        """Get the fully-qualified name of the character input source."""
        return type(self).__name__

    @abstractmethod
    def choose_move(
        self,
        mode: GameMode,
        view: PlayerView,
        legal_moves: list[Move],
        evaluator: Callable[[PlayerView, Move], PlayerView],
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


class NoOpInputSource(CharacterInputSource):
    """
    A no-op input source, which raises an error if ever used.

    The Apologies library is designed with a synchronous callback model in mind.  If your
    application uses a different model, you may use lower-level methods to interact with
    the game engine directly, rather than getting user input from a callback.  In that case,
    you will use this character input source.  If you get an error, you'll know that you've
    done something wrong.
    """

    def choose_move(
        self, _mode: GameMode, _view: PlayerView, _moves: list[Move], _evaluator: Callable[[PlayerView, Move], PlayerView]
    ) -> Move:
        raise NotImplementedError


class RandomInputSource(CharacterInputSource):
    """
    A source of input for a character which chooses randomly from among legal moves.
    """

    def choose_move(  # noqa: PLR6301
        self,
        _mode: GameMode,
        _view: PlayerView,
        legal_moves: list[Move],
        _evaluator: Callable[[PlayerView, Move], PlayerView],
    ) -> Move:
        """Randomly choose the next move for a character."""
        return random.choice(legal_moves)


# noinspection PyMethodMayBeStatic
class RewardInputSource(CharacterInputSource):
    """
    A source of input for a character which chooses its next move based on a reward calculation.
    """

    @abstractmethod
    def calculate(
        self,
        view: PlayerView,
        move: Move,
        evaluator: Callable[[PlayerView, Move], PlayerView],
    ) -> tuple[Move, float]:
        """Calculate the reward associated with a move, returning a tuple of (Move, reward)."""

    def choose_move(
        self,
        _mode: GameMode,
        view: PlayerView,
        legal_moves: list[Move],
        evaluator: Callable[[PlayerView, Move], PlayerView],
    ) -> Move:
        """Choose the next move for a player by evaluating and scoring the available moves."""
        evaluated = [self.calculate(view, move, evaluator) for move in legal_moves]  # calculate a reward for each move
        evaluated.sort(reverse=True, key=operator.itemgetter(1))  # sort the highest-scoring move to the top
        return evaluated[0][0]  # return the highest-scoring move


# noinspection PyMethodMayBeStatic
class RewardV1InputSource(RewardInputSource):
    """
    A source of input for a character which chooses its next move based on the RewardCalculatorV1.
    """

    calculator = RewardCalculatorV1()

    def calculate(
        self,
        view: PlayerView,
        move: Move,
        evaluator: Callable[[PlayerView, Move], PlayerView],
    ) -> tuple[Move, float]:
        """Calculate the reward associated with a move, returning a tuple of (Move, reward)."""
        return move, self.calculator.calculate(evaluator(view, move))


# noinspection PyCallingNonCallable
def source(name: str) -> CharacterInputSource:
    """
    Create a character input source by name.

    As a special case, if the name is not fully-qualified, we will assume "apologies.source".

    Args:
        name(str): Fully-qualified name of the source, like "apologies.source.RandomInputSource"

    Returns:
        CharacterInputSource: An instance of the named source

    Raises:
        ValueError: If the named source does not exist or is not a CharacterInputSource
    """
    if "." not in name:
        name = f"apologies.source.{name}"
    cls = locate(name)
    if not issubclass(cls, CharacterInputSource):  # type: ignore[arg-type]
        msg = f"{name} is not a CharacterInputSource"
        raise TypeError(msg)
    return cls()  # type: ignore[operator,no-any-return]
