# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:

"""
Implements rules related to game play.
"""

from enum import Enum
from typing import List, Optional, Sequence

import attr

from .game import ADULT_HAND, BOARD_SQUARES, SAFE_SQUARES, Card, CardType, Game, GameMode, Pawn, PlayerColor, PlayerView, Position

# The start squares for each color
_START_SQUARE = {
    PlayerColor.RED: 4,
    PlayerColor.BLUE: 19,
    PlayerColor.YELLOW: 34,
    PlayerColor.GREEN: 49,
}

# The turn squares for each color, where forward movement turns into the safe zone
_TURN_SQUARE = {
    PlayerColor.RED: 2,
    PlayerColor.BLUE: 17,
    PlayerColor.YELLOW: 32,
    PlayerColor.GREEN: 47,
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

    MOVE_FROM_START = "Move from start"  # Move a pawn from start
    MOVE_FORWARD = "Move forward"  # Move a pawn forward a certain number of spaces
    MOVE_BACKARD = "Move backward"  # Move a pawn backward a certain number of spaces
    CHANGE_PLACES = "Change places"  # Change places, swapping two pawns on the board
    BUMP_TO_START = "Bump to start"  # Move a pawn from start, bumping another pawn off the board


@attr.s
class Action:
    """An action that can be taken as part of a move."""

    actiontype = attr.ib(type=ActionType)
    mine = attr.ib(type=Pawn)
    theirs = attr.ib(default=None, type=Optional[Pawn])
    squares = attr.ib(default=None, type=Optional[int])


@attr.s
class Move:

    """
    A player's move on the board, which consists of one or more actions

    Attributes:
        card(Card): the card that is being played by this move
        actions(:obj: List of :obj: Action): List of actions to execute
    """

    card = attr.ib(type=Card)
    actions = attr.ib(type=Sequence[Action])


# noinspection PyMethodMayBeStatic
class BoardRules:

    """
    Rules related to the way the board works.
    """

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
        if not pawn.position.home:  # there are no legal moves for a pawn in home
            if card.cardtype == CardType.CARD_1:
                return BoardRules._construct_legal_moves_1(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_2:
                return BoardRules._construct_legal_moves_2(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_3:
                return BoardRules._construct_legal_moves_3(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_4:
                return BoardRules._construct_legal_moves_4(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_5:
                return BoardRules._construct_legal_moves_5(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_7:
                return BoardRules._construct_legal_moves_7(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_8:
                return BoardRules._construct_legal_moves_8(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_10:
                return BoardRules._construct_legal_moves_10(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_11:
                return BoardRules._construct_legal_moves_11(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_12:
                return BoardRules._construct_legal_moves_12(color, card, pawn, all_pawns)
            elif card.cardtype == CardType.CARD_APOLOGIES:
                return BoardRules._construct_legal_moves_apologies(color, card, pawn, all_pawns)
        return []

    # pylint: disable=no-else-raise,too-many-branches
    def position(self, color: PlayerColor, position: Position, squares: int) -> Position:
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
                    return self.position(color, position.copy().move_to_square(_TURN_SQUARE[color]), squares + position.safe + 1)
        elif position.square is not None:
            if squares == 0:
                return position.copy()
            elif squares > 0:
                if position.square + squares < BOARD_SQUARES:
                    if position.square <= _TURN_SQUARE[color] and position.square + squares > _TURN_SQUARE[color]:
                        return self.position(
                            color, position.copy().move_to_safe(0), squares - (_TURN_SQUARE[color] - position.square) - 1
                        )
                    else:
                        return position.copy().move_to_square(position.square + squares)
                else:  # handle turning the corner
                    return self.position(color, position.copy().move_to_square(0), squares - (BOARD_SQUARES - position.square))
            else:  # squares < 0
                if position.square + squares >= 0:
                    return position.copy().move_to_square(position.square + squares)
                else:  # handle turning the corner
                    return self.position(color, position.copy().move_to_square(BOARD_SQUARES - 1), squares + position.square + 1)
        else:
            raise ValueError("Position is in an illegal state")

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_1(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_1, possibly empty."""
        moves: List[Move] = []
        if pawn.position.start:
            # A pawn can move out from start if that position is not occupied by another
            # pawn of the same color.
            pass
        else:
            # A pawn can move forward 1 space if that position is not occupied by another
            # pawn of the same color and does not move it past home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_2(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_2, possibly empty."""
        moves: List[Move] = []
        if pawn.position.start:
            # A pawn can move out from start if that position is not occupied by another
            # pawn of the same color.
            pass
        else:
            # A pawn can move forward 2 spaces if that position is not occupied by
            # another pawn of the same color and does not move it past home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_3(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_3, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 3 spaces if that position is not
            # occupied by another pawn of the same color and does not move it past home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_4(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_4, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move backward 4 spaces if that position is not
            # occupied by another pawn of the same color and does not move it past home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_5(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_5, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 5 spaces if that position is not
            # occupied by another pawn of the same color and does not move it past home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_7(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_7, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 7 spaces or split its move with another
            # pawn of the same color as long as their positions are not occupied by another
            # pawns of the same color and they do not move past home
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_8(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_8, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 8 spaces if that position is not
            # occupied by another pawn of the same color and does not move it past home
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_10(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_10, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 10 spaces or backward 1 space if that
            # position is not occupied by another pawn of the same color and does not move
            # it past home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_11(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_11, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 11 spaces if that position is not
            # occupied by another pawn of the same color and does not move it past home or
            # may switch with another pawn of a different color that is not in start or
            # home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_12(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_12, possibly empty."""
        moves: List[Move] = []
        if not pawn.position.start:
            # A pawn on the board can move forward 12 spaces if that position is not
            # occupied by another pawn of the same color and does not move it past home.
            pass
        return moves

    # pylint: disable=unused-argument   # TODO: remove this
    @staticmethod
    def _construct_legal_moves_apologies(color: PlayerColor, card: Card, pawn: Pawn, all_pawns: List[Pawn]) -> List[Move]:
        """Return the set of legal moves for a pawn using CARD_APOLOGIES, possibly empty."""
        moves: List[Move] = []
        if pawn.position.start:
            # A pawn in start may switch with another pawn of a different color that is not
            # in start or home.
            for other in [
                other for other in all_pawns if other.color != pawn.color and not other.position.home and not other.position.start
            ]:
                action = Action(ActionType.BUMP_TO_START, mine=pawn, theirs=other)
                move = Move(card, [action])
                moves.append(move)
        return moves


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

        Note that legal moves describe both the move that the player would make, as well
        as the end state of the pawns affected by that move.  For instance, the player
        might move their green pawn to the top of a blue side.  However, the end state
        is that that the pawn moves to the bottom of the slide and any other pawns on
        the slide are moved back to their start.  So, there is enough information
        encapulated in the move to fully execute it, without doing any other analysis.

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

    def execute_move(self, game: Game, color: PlayerColor, move: Move) -> None:
        """
            Execute a player's move, updating game state.

            Args:
                game(Game): Game to operate on
                color(PlayerColor): Color of the player associated with the move
                move(Move): Move to validate

            Raises:
                ValidationError: If the move is not valid
            """

    # TODO: implement Rules.execute_move()

    @staticmethod
    def _setup_adult_mode(game: Game) -> None:
        """Setup adult mode at the start of the game, which moves some pieces and deals some cards."""
        for player in game.players.values():
            player.pawns[0].position.move_to_square(_START_SQUARE[player.color])
        for _ in range(ADULT_HAND):
            for player in game.players.values():
                player.hand.append(game.deck.draw())
