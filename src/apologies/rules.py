# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implements rules related to game play.
"""

import uuid
from enum import Enum
from typing import List, Optional

import attr

from .game import (
    ADULT_HAND,
    BOARD_SQUARES,
    CIRCLE,
    DRAW_AGAIN,
    SAFE_SQUARES,
    SLIDE,
    TURN,
    Card,
    CardType,
    Game,
    GameMode,
    Pawn,
    Player,
    PlayerColor,
    PlayerView,
    Position,
)


class ActionType(Enum):
    """Enumeration of all actions that a character can take."""

    MOVE_TO_START = "Move to start"  # Move a pawn back to its start area
    MOVE_TO_POSITION = "Move to position"  # Move a pawn to a specific position on the board


@attr.s
class Action:
    """
    An action that can be taken as part of a move.

    Attributes:
        actiontype(ActionType): The type of action
        pawn(Pawn): The pawn that the action operates on
        position(Position): Optionally, a position the pawn should move to
    """

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
        card(Card): The card that is being played by this move
        actions(List[Action]): List of actions to execute
        side_effects(List[Action]): List of side effects that occurred as a result of the actions
        id(str): Identifier for this move, which must be unique among all legal moves this move is grouped with
    """

    card = attr.ib(type=Card)
    actions = attr.ib(type=List[Action])
    side_effects = attr.ib(type=List[Action])
    id = attr.ib(type=str)

    @id.default
    def _default_id(self) -> str:
        return uuid.uuid4().hex

    @side_effects.default
    def _default_side_effects(self) -> List[Action]:
        return []


# noinspection PyMethodMayBeStatic
class BoardRules:

    """
    Rules related to the way the board works.
    """

    # pylint: disable=too-many-return-statements
    def construct_legal_moves(self, color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """
        Return the set of legal moves for a pawn using a card, possibly empty.

        Attributes:
            card(Card): Card to be played
            pawn(Pawn): Pawn that the card will be applied to
            all_pawns(List[Pawn]): All pawns on the board, including the one to be played

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

    @staticmethod
    def distance_to_home(pawn: Pawn) -> int:
        """Return the distance to home for this pawn, a number of squares when moving forward."""
        if pawn.position.home:
            return 0
        elif pawn.position.start:
            return 65
        elif pawn.position.safe is not None:
            return SAFE_SQUARES - pawn.position.safe
        else:
            circle = CIRCLE[pawn.color].square
            turn = TURN[pawn.color].square
            square = pawn.position.square
            square_to_corner = BOARD_SQUARES - square  # type: ignore
            corner_to_turn = turn
            turn_to_home = SAFE_SQUARES + 1
            total = square_to_corner + corner_to_turn + turn_to_home  # type: ignore
            if turn < square < circle:  # type: ignore
                return total
            if total < 65:
                return total
            else:
                return total - 60

    # noinspection PyChainedComparisons
    # pylint: disable=too-many-branches,too-many-return-statements,line-too-long
    @staticmethod
    def _position(color: PlayerColor, position: Position, squares: int) -> Position:
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
                    return BoardRules._position(color, position.copy().move_to_square(TURN[color].square), squares + position.safe + 1)  # type: ignore
        elif position.square is not None:
            if squares == 0:
                return position.copy()
            elif squares > 0:
                if position.square + squares < BOARD_SQUARES:
                    if position.square <= TURN[color].square and position.square + squares > TURN[color].square:  # type: ignore
                        return BoardRules._position(color, position.copy().move_to_safe(0), squares - (TURN[color].square - position.square) - 1)  # type: ignore
                    else:
                        return position.copy().move_to_square(position.square + squares)
                else:  # handle turning the corner
                    return BoardRules._position(
                        color, position.copy().move_to_square(0), squares - (BOARD_SQUARES - position.square)
                    )
            else:  # squares < 0
                if position.square + squares >= 0:
                    return position.copy().move_to_square(position.square + squares)
                else:  # handle turning the corner
                    return BoardRules._position(
                        color, position.copy().move_to_square(BOARD_SQUARES - 1), squares + position.square + 1
                    )
        else:
            raise ValueError("Position is in an illegal state")

    @staticmethod
    def _construct_legal_moves_1(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_1, possibly empty."""
        moves: List[Move] = []
        moves += BoardRules._move_circle(color, card, pawn, all_pawns)
        moves += BoardRules._move_simple(color, card, pawn, all_pawns, 1)
        return moves

    @staticmethod
    def _construct_legal_moves_2(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_2, possibly empty."""
        moves: List[Move] = []
        moves += BoardRules._move_circle(color, card, pawn, all_pawns)
        moves += BoardRules._move_simple(color, card, pawn, all_pawns, 2)
        return moves

    @staticmethod
    def _construct_legal_moves_3(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_3, possibly empty."""
        return BoardRules._move_simple(color, card, pawn, all_pawns, 3)

    @staticmethod
    def _construct_legal_moves_4(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_4, possibly empty."""
        return BoardRules._move_simple(color, card, pawn, all_pawns, -4)

    @staticmethod
    def _construct_legal_moves_5(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_5, possibly empty."""
        return BoardRules._move_simple(color, card, pawn, all_pawns, 5)

    @staticmethod
    def _construct_legal_moves_7(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_7, possibly empty."""
        moves: List[Move] = []
        moves += BoardRules._move_simple(color, card, pawn, all_pawns, 7)
        moves += BoardRules._move_split(color, card, pawn, all_pawns)
        return moves

    @staticmethod
    def _construct_legal_moves_8(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_8, possibly empty."""
        return BoardRules._move_simple(color, card, pawn, all_pawns, 8)

    @staticmethod
    def _construct_legal_moves_10(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_10, possibly empty."""
        moves: List[Move] = []
        moves += BoardRules._move_simple(color, card, pawn, all_pawns, 10)
        moves += BoardRules._move_simple(color, card, pawn, all_pawns, -1)
        return moves

    @staticmethod
    def _construct_legal_moves_11(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_11, possibly empty."""
        moves: List[Move] = []
        moves += BoardRules._move_swap(color, card, pawn, all_pawns)
        moves += BoardRules._move_simple(color, card, pawn, all_pawns, 11)
        return moves

    @staticmethod
    def _construct_legal_moves_12(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_12, possibly empty."""
        return BoardRules._move_simple(color, card, pawn, all_pawns, 12)

    @staticmethod
    def _construct_legal_moves_apologies(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_APOLOGIES, possibly empty."""
        return BoardRules._move_apologies(color, card, pawn, all_pawns)

    @staticmethod
    def _find_pawn(all_pawns: List[Pawn], position: Position) -> Optional[Pawn]:
        """Return the first pawn at the indicated position, or None."""
        for pawn in all_pawns:
            if pawn.position == position:
                return pawn
        return None

    @staticmethod
    def _move_circle(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        # For start-related cards, a pawn in the start area can move to the associated
        # circle position if that position is not occupied by another pawn of the same color.
        moves: List[Move] = []
        if pawn.position.start:
            conflict = BoardRules._find_pawn(all_pawns, CIRCLE[color])
            if not conflict:
                moves.append(Move(card, actions=[Action(ActionType.MOVE_TO_POSITION, pawn, CIRCLE[color].copy())]))
            elif conflict and conflict.color != color:
                moves.append(
                    Move(
                        card,
                        actions=[Action(ActionType.MOVE_TO_POSITION, pawn, CIRCLE[color].copy())],
                        side_effects=[Action(ActionType.MOVE_TO_START, conflict)],
                    )
                )
        return moves

    @staticmethod
    def _move_simple(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn], squares: int) -> List[Move]:
        # For most cards, a pawn on the board can move forward or backward if the
        # resulting position is not occupied by another pawn of the same color.
        moves: List[Move] = []
        if pawn.position.square is not None or pawn.position.safe is not None:
            try:
                target = BoardRules._position(color, pawn.position, squares)
                if target.home or target.start:  # by definition, there can't be a conflict going to home or start
                    moves.append(Move(card, actions=[Action(ActionType.MOVE_TO_POSITION, pawn, target)]))
                else:
                    conflict = BoardRules._find_pawn(all_pawns, target)
                    if not conflict:
                        moves.append(Move(card, actions=[Action(ActionType.MOVE_TO_POSITION, pawn, target)]))
                    elif conflict and conflict.color != color:
                        moves.append(
                            Move(
                                card,
                                actions=[Action(ActionType.MOVE_TO_POSITION, pawn, target)],
                                side_effects=[Action(ActionType.MOVE_TO_START, conflict)],
                            )
                        )
            except ValueError as ignored:
                pass  # if the requested position is not legal, then just ignore it
        return moves

    @staticmethod
    def _move_split(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        # For the 7 card, we can split up the move between two different pawns.
        # Any combination of 7 forward moves is legal, as long as the resulting position
        # is not occupied by another pawn of the same color.
        moves: List[Move] = []
        for other in all_pawns:
            if other != pawn and other.color == color and not other.position.home and not other.position.start:
                for (left, right) in [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]:  # legal ways to split up a move of 7
                    left_moves = BoardRules._move_simple(color, card, pawn, [p for p in all_pawns if p != other], left)
                    right_moves = BoardRules._move_simple(color, card, other, [p for p in all_pawns if p != other], right)
                    if left_moves and right_moves:
                        moves.append(
                            Move(
                                card,
                                actions=left_moves[0].actions + right_moves[0].actions,
                                side_effects=left_moves[0].side_effects + right_moves[0].side_effects,
                            )
                        )
        return moves

    @staticmethod
    def _move_swap(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        # For the 11 card, a pawn on the board can swap with another pawn of a different
        # color, as long as that pawn is outside of the start area, safe area, or home area.
        moves: List[Move] = []
        if pawn.position.square is not None:  # pawn is on the board
            for swap in all_pawns:
                if swap.color != color and not swap.position.home and not swap.position.start and swap.position.safe is None:
                    moves.append(
                        Move(
                            card,
                            actions=[
                                Action(ActionType.MOVE_TO_POSITION, pawn, swap.position.copy()),
                                Action(ActionType.MOVE_TO_POSITION, swap, pawn.position.copy()),
                            ],
                        )
                    )
        return moves

    @staticmethod
    def _move_apologies(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        # For the Apologies card, a pawn in start can swap with another pawn of a different
        # color, as long as that pawn is outside of the start area, safe area, or home area.
        moves: List[Move] = []
        if pawn.position.start:
            for swap in all_pawns:
                if swap.color != color and not swap.position.home and not swap.position.start and swap.position.safe is None:
                    moves.append(
                        Move(
                            card,
                            actions=[
                                Action(ActionType.MOVE_TO_POSITION, pawn, swap.position.copy()),
                                Action(ActionType.MOVE_TO_START, swap),
                            ],
                        )
                    )
        return moves

    # pylint: disable=too-many-nested-blocks
    @staticmethod
    def _augment_with_slides(all_pawns: List[Pawn], moves: List[Move]) -> None:
        """Augument any legal moves with additional side-effects that occur as a result of slides."""
        for move in moves:
            for action in move.actions:
                if action.actiontype == ActionType.MOVE_TO_POSITION:  # look at any move to a position on the board
                    for color in [color for color in PlayerColor if color != action.pawn.color]:  # any color other than the pawn's
                        for (start, end) in SLIDE[color]:  # look at all slides with this color
                            if action.position.square == start:  # if the pawn landed on the start of the slide
                                action.position.move_to_square(end)  # move the pawn to the end of the slide
                                for square in range(start + 1, end + 1):  # and then bump any pawns that were already on the slide
                                    # Note: in this one case, a pawn can bump another pawn of the same color
                                    pawn = BoardRules._find_pawn(all_pawns, Position().move_to_square(square))
                                    if pawn:
                                        bump = Action(ActionType.MOVE_TO_START, pawn)
                                        if bump not in move.actions:
                                            move.side_effects.append(bump)


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
    def _default_board_rules(self) -> BoardRules:
        return BoardRules()

    # noinspection PyMethodMayBeStatic
    def draw_again(self, card: Card) -> bool:
        """Whether the player gets to draw again based on the passed-in card."""
        return DRAW_AGAIN[card.cardtype]

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
            List[Move]: Set of legal moves for the player, as described above.
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
    def execute_move(self, game: Game, player: Player, move: Move) -> None:
        """
        Execute a player's move, updating game state.

        Args:
            game(Game): Game to operate on
            player(Player): Color of the player associated with the move
            move(Move): Move to validate
        """
        log = "Played card %s: [ " % move.card.cardtype.value
        for action in move.actions + move.side_effects:  # execute actions, then side-effects, in order
            # Keep in mind that the pawn on the action is a different object than the pawn in the game
            pawn = game.players[action.pawn.color].pawns[action.pawn.index]
            if action.actiontype == ActionType.MOVE_TO_START:
                pawn.position.move_to_start()
                log += "%s->start, " % pawn.name
            elif action.actiontype == ActionType.MOVE_TO_POSITION:
                pawn.position.move_to_position(action.position)
                log += "%s, " % pawn
        log += "]"
        game.track(log, player, move.card)
        if game.completed:
            game.track("Game completed: winner is %s after %d turns" % (game.winner.color.value, game.winner.turns))  # type: ignore

    @staticmethod
    def evaluate_move(view: PlayerView, move: Move) -> PlayerView:
        """
        Construct the new player view that results from executing the passed-in move.

        This is equivalent to execute_move() but has no permanent effect on the game.  It's intended for
        use by a character, to evaluate the results of each legal move.

        Args:
            view(PlayerView):
            move(Move):

        Returns:
            PlayerView: The new state after executing the move.
        """
        result = view.copy()
        for action in move.actions + move.side_effects:  # execute actions, then side-effects, in order
            # Keep in mind that the pawn on the action is a different object than the pawn in the view
            pawn = result.get_pawn(action.pawn)
            if pawn:  # if the pawn isn't valid, just ignore it
                if action.actiontype == ActionType.MOVE_TO_START:
                    pawn.position.move_to_start()
                elif action.actiontype == ActionType.MOVE_TO_POSITION:
                    pawn.position.move_to_position(action.position)
        return result

    @staticmethod
    def _setup_adult_mode(game: Game) -> None:
        """Setup adult mode at the start of the game, which moves some pieces and deals some cards."""
        for player in game.players.values():
            player.pawns[0].position.move_to_position(CIRCLE[player.color])
        for _ in range(ADULT_HAND):
            for player in game.players.values():
                player.hand.append(game.deck.draw())
