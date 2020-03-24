# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implements rules related to game play.
"""

from enum import Enum
from typing import List, Optional

import attr

from .game import ADULT_HAND, BOARD_SQUARES, SAFE_SQUARES, Card, CardType, Game, GameMode, Pawn, PlayerColor, PlayerView, Position

# The start circles for each color
_CIRCLE = {
    PlayerColor.RED: Position().move_to_square(4),
    PlayerColor.BLUE: Position().move_to_square(19),
    PlayerColor.YELLOW: Position().move_to_square(34),
    PlayerColor.GREEN: Position().move_to_square(49),
}

# The turn squares for each color, where forward movement turns into the safe zone
_TURN = {
    PlayerColor.RED: Position().move_to_square(2),
    PlayerColor.BLUE: Position().move_to_square(17),
    PlayerColor.YELLOW: Position().move_to_square(32),
    PlayerColor.GREEN: Position().move_to_square(47),
}

# The slide start/end positions for each color
_SLIDE = {
    PlayerColor.RED: ((1, 4), (9, 13)),
    PlayerColor.BLUE: ((16, 19), (24, 28)),
    PlayerColor.YELLOW: ((31, 34), (39, 43)),
    PlayerColor.GREEN: ((46, 49), (54, 58)),
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


class ActionType(Enum):
    """Enumeration of all actions that a character can take."""

    MOVE_TO_START = "Move to start"  # Move a pawn back to its start area
    MOVE_TO_POSITION = "Move to position"  # Move a pawn to a specific square on the board


@attr.s
class Action:
    """An action that can be taken as part of a move."""

    actiontype = attr.ib(type=ActionType)
    pawn = attr.ib(type=Pawn)
    position = attr.ib(default=None, type=Position)


@attr.s
class Move:

    """
    A player's move on the board, which consists of one or more actions.

    Note that the actions associated with a move include both the immediate actions that the player
    chose (such as moving a pawn from start or swapping places with a different pawn), but also
    any side-effects (such as pawns that are bumped back to start because of a slide).  As a result,
    executing a move becomes very easy and no validation is required.  All of the work is done
    up-front.

    Attributes:
        card(Card): the card that is being played by this move
        actions(:obj: List of :obj: Action): List of actions to execute
    """

    card = attr.ib(type=Card)
    actions = attr.ib(type=List[Action])


# noinspection PyMethodMayBeStatic
class BoardRules:

    """
    Rules related to the way the board works.
    """

    # noinspection PyChainedComparisons
    # pylint: disable=no-else-raise,no-else-return,too-many-branches,too-many-return-statements,line-too-long
    @staticmethod
    def position(color: PlayerColor, position: Position, squares: int) -> Position:
        """
        Calculate the new position for a forward or backwards move, taking into account safe zone turns but disregarding slides.
        """
        if position.home or position.start:
            raise ValueError("Pawn in home or start may not move.")
        elif position.safe is not None:
            if squares == 0:
                return position.copy()
            elif squares > 0:
                if position.safe + squares < SAFE_SQUARES:
                    return position.copy().move_to_safe(position.safe + squares)
                elif position.safe + squares == SAFE_SQUARES:
                    return position.copy().move_to_home()
                else:
                    raise ValueError("Pawn cannot move past home.")
            else:  # squares < 0
                if position.safe + squares >= 0:
                    return position.copy().move_to_safe(position.safe + squares)
                else:  # handle moving back out of the safe area
                    return BoardRules.position(color, position.copy().move_to_square(_TURN[color].square), squares + position.safe + 1)  # type: ignore
        elif position.square is not None:
            if squares == 0:
                return position.copy()
            elif squares > 0:
                if position.square + squares < BOARD_SQUARES:
                    if position.square <= _TURN[color].square and position.square + squares > _TURN[color].square:  # type: ignore
                        return BoardRules.position(color, position.copy().move_to_safe(0), squares - (_TURN[color].square - position.square) - 1)  # type: ignore
                    else:
                        return position.copy().move_to_square(position.square + squares)
                else:  # handle turning the corner
                    return BoardRules.position(
                        color, position.copy().move_to_square(0), squares - (BOARD_SQUARES - position.square)
                    )
            else:  # squares < 0
                if position.square + squares >= 0:
                    return position.copy().move_to_square(position.square + squares)
                else:  # handle turning the corner
                    return BoardRules.position(
                        color, position.copy().move_to_square(BOARD_SQUARES - 1), squares + position.square + 1
                    )
        else:
            raise ValueError("Position is in an illegal state")

    # pylint: disable=no-else-return,too-many-return-statements
    def construct_legal_moves(self, color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """
        Return the set of legal moves for a pawn using a card, possibly empty.

        Attributes:
            card(Card): Card to be played
            pawn(Pawn): Pawn that the card will be applied to
            all_pawns(:obj: List of :obj: Pawn): All pawns on the board, including the one to be played

        Return:
            Set of legal moves for the pawn using the card.
        """
        moves: List[Move] = []
        if not pawn.position.home:  # there are no legal moves for a pawn in home
            if card.cardtype == CardType.CARD_1:
                moves += BoardRules._construct_legal_moves_1(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_2:
                moves += BoardRules._construct_legal_moves_2(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_3:
                moves += BoardRules._construct_legal_moves_3(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_4:
                moves += BoardRules._construct_legal_moves_4(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_5:
                moves += BoardRules._construct_legal_moves_5(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_7:
                moves += BoardRules._construct_legal_moves_7(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_8:
                moves += BoardRules._construct_legal_moves_8(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_10:
                moves += BoardRules._construct_legal_moves_10(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_11:
                moves += BoardRules._construct_legal_moves_11(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_12:
                moves += BoardRules._construct_legal_moves_12(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_APOLOGIES:
                moves += BoardRules._construct_legal_moves_apologies(color, card, pawn, all_pawns)
        BoardRules._augment_with_slides(all_pawns, moves)
        return moves

    # pylint: disable=too-many-nested-blocks
    @staticmethod
    def _augment_with_slides(all_pawns: List[Pawn], moves: List[Move]) -> None:
        """Augument any legal moves with additional side-effects that occur as a result of sliding."""
        for move in moves:
            for action in move.actions[:]:  # operate on a copy so we can modify move.actions if necessary
                if action.actiontype == ActionType.MOVE_TO_POSITION:  # look at any move to a position on the board
                    for color in [color for color in PlayerColor if color != action.pawn.color]:  # any color other than the pawn's
                        for (start, end) in _SLIDE[color]:  # look at all slides with this color
                            if action.pawn.position.square == start:  # if the pawn landed on the start of the slide
                                action.pawn.position.move_to_square(end)  # move the pawn to the end of the slide
                                for square in range(start + 1, end + 1):  # and then bump any pawns that were already on the slide
                                    pawn = BoardRules._find_pawn(all_pawns, Position().move_to_square(square))
                                    if pawn:
                                        bump = Action(ActionType.MOVE_TO_START, pawn)
                                        if bump not in move.actions:
                                            move.actions.append(bump)

    @staticmethod
    def _construct_legal_moves_1(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_1, possibly empty."""
        moves: List[Move] = []
        if pawn.position.start:
            moves += BoardRules.move_start(color, card, pawn, all_pawns)
        moves += BoardRules.move_simple(color, card, pawn, all_pawns, 1)
        return moves

    @staticmethod
    def _construct_legal_moves_2(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_2, possibly empty."""
        moves: List[Move] = []
        if pawn.position.start:
            moves += BoardRules.move_start(color, card, pawn, all_pawns)
        moves += BoardRules.move_simple(color, card, pawn, all_pawns, 2)
        return moves

    @staticmethod
    def _construct_legal_moves_3(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_3, possibly empty."""
        return BoardRules.move_simple(color, card, pawn, all_pawns, 3)

    @staticmethod
    def _construct_legal_moves_4(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_4, possibly empty."""
        return BoardRules.move_simple(color, card, pawn, all_pawns, -4)

    @staticmethod
    def _construct_legal_moves_5(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_5, possibly empty."""
        return BoardRules.move_simple(color, card, pawn, all_pawns, 5)

    @staticmethod
    def _construct_legal_moves_7(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_7, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 7 spaces or split its move with another pawn of the same color.
            moves += BoardRules.move_simple(color, card, pawn, all_pawns, 7)
            for other in all_pawns:
                if other != pawn and other.color == color and not other.position.home and not other.position.start:
                    for (left, right) in [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]:  # legal ways to split up a move of 7
                        moves += BoardRules.move_simple(color, card, pawn, all_pawns, left)
                        moves += BoardRules.move_simple(color, card, other, all_pawns, right)
        return moves

    @staticmethod
    def _construct_legal_moves_8(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_8, possibly empty."""
        return BoardRules.move_simple(color, card, pawn, all_pawns, 8)

    @staticmethod
    def _construct_legal_moves_10(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_10, possibly empty."""
        return BoardRules.move_simple(color, card, pawn, all_pawns, 10)

    @staticmethod
    def _construct_legal_moves_11(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_11, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            moves += BoardRules.move_swap(color, card, pawn, all_pawns)
        moves += BoardRules.move_simple(color, card, pawn, all_pawns, 11)
        return moves

    @staticmethod
    def _construct_legal_moves_12(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_12, possibly empty."""
        return BoardRules.move_simple(color, card, pawn, all_pawns, 12)

    @staticmethod
    def _construct_legal_moves_apologies(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_APOLOGIES, possibly empty."""
        moves: List[Move] = []
        if pawn.position.start:
            moves += BoardRules.move_swap(color, card, pawn, all_pawns)
        return moves

    @staticmethod
    def move_start(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        # For start-related cards, a pawn in the start area can move to the associated
        # start square if that position is not occupied by another pawn of the same color.
        if pawn.position.start:
            conflict = BoardRules._find_pawn(all_pawns, _CIRCLE[color])
            if not conflict:
                return [Move(card, [Action(ActionType.MOVE_TO_POSITION, pawn, _CIRCLE[color]),],)]
            elif conflict and conflict.color != color:
                return [
                    Move(
                        card,
                        [Action(ActionType.MOVE_TO_START, conflict), Action(ActionType.MOVE_TO_POSITION, pawn, _CIRCLE[color]),],
                    )
                ]
        return []

    @staticmethod
    def move_simple(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn], squares: int) -> List[Move]:
        # For most cards, a pawn on the board can move forward or backward if that position is
        # not occupied by another pawn of the same color and does not move the pawn past home.
        if not pawn.position.start:
            target = BoardRules.position(color, pawn.position, squares)
            conflict = BoardRules._find_pawn(all_pawns, target)
            if not conflict:
                return [Move(card, [Action(ActionType.MOVE_TO_POSITION, pawn, target),],)]
            elif conflict and conflict.color != color:
                return [
                    Move(card, [Action(ActionType.MOVE_TO_START, conflict), Action(ActionType.MOVE_TO_POSITION, pawn, target),],)
                ]
        return []

    @staticmethod
    def move_swap(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        # For swap-related cards, a pawn on the board can swap with another pawn of a different
        # color, as long as that pawn is outside of the start area, safe area, or home area.
        moves: List[Move] = []
        for candidate in all_pawns:
            if (
                candidate.color != color
                and not candidate.position.home
                and not candidate.position.start
                and candidate.position.safe is None
            ):
                moves.append(
                    Move(
                        card,
                        [
                            Action(ActionType.MOVE_TO_POSITION, pawn, candidate.position),
                            Action(ActionType.MOVE_TO_POSITION, candidate, pawn.position),
                        ],
                    )
                )
        return moves

    @staticmethod
    def _find_pawn(all_pawns: List[Pawn], position: Position) -> Optional[Pawn]:
        """Return the first pawn at the indicated position, or None."""
        for pawn in all_pawns:
            if pawn.position == position:
                return pawn
        return None


# noinspection PyProtectedMember
@attr.s
class Rules:

    """
    Implements rules related to game play.

    Attributes:
        mode(GameMode): The game mode
    """

    mode = attr.ib(type=GameMode)
    _board_rules = attr.ib(init=False, type=BoardRules)

    @_board_rules.default
    def _init_board_rules(self) -> BoardRules:
        return BoardRules()

    # noinspection PyMethodMayBeStatic
    def draw_again(self, card: Card) -> bool:
        """Whether the player gets to draw again based on the passed-in card."""
        return _DRAW_AGAIN[card.cardtype]

    def start_game(self, game: Game) -> None:
        """
        Start the game.

        Args:
            game(Game): Game to operate on
        """
        if game.started:
            raise ValueError("Game is already started")
        game.track("Game started with mode: %s" % self.mode)
        if self.mode == GameMode.ADULT:
            Rules._setup_adult_mode(game)

    def construct_legal_moves(self, view: PlayerView, card: Optional[Card] = None) -> List[Move]:
        """
        Return the set of all legal moves for a player and its opponents.

        Attributes:
            view(PlayerView): Player-specific view of the game
            card(Card, optional): The card to play, or None if move should come from player's hand

        Returns:
            Set of legal moves for the player, as described above.
        """
        moves: List[Move] = []
        all_pawns = view.all_pawns()
        for played in [card] if card else view.player.hand:
            for pawn in view.player.pawns:
                for move in self._board_rules.construct_legal_moves(view.player.color, played, pawn, all_pawns):
                    if move not in moves:  # filter out duplicates
                        moves.append(move)
        if not moves:  # if there are no legal moves, then forfeit (discarding one card) becomes the only allowable move
            for played in [card] if card else view.player.hand:
                moves.append(Move(played, []))
        if not moves:  # if there are still no legal moves, then this is an internal error
            raise ValueError("Internal error: could not construct any legal moves")
        return moves

    # noinspection PyMethodMayBeStatic
    def execute_move(self, game: Game, color: PlayerColor, move: Move) -> None:
        """
        Execute a player's move, updating game state.

        Args:
            game(Game): Game to operate on
            color(PlayerColor): Color of the player associated with the move
            move(Move): Move to validate
        """
        for action in move.actions:
            pawn = game.players[color].pawns[action.pawn.index]
            if action.actiontype == ActionType.MOVE_TO_START:
                pawn.position.move_to_start()
            elif action.actiontype == ActionType.MOVE_TO_POSITION:
                pawn.position.move_to_position(action.position)

    @staticmethod
    def _setup_adult_mode(game: Game) -> None:
        """Setup adult mode at the start of the game, which moves some pieces and deals some cards."""
        for player in game.players.values():
            player.pawns[0].position.move_to_position(_CIRCLE[player.color])
        for _ in range(ADULT_HAND):
            for player in game.players.values():
                player.hand.append(game.deck.draw())
