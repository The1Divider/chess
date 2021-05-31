from __future__ import annotations

from contextlib import suppress
from copy import deepcopy
from enum import Enum, auto

from pieces import *

# Typing and aliases
WHITE, BLACK = "WHITE", "BLACK"
piece_colour = Literal["WHITE", "BLACK"]


PAWN = Literal["P", "p"]
ROOK = Literal["R", "r"]
KNIGHT = Literal["N", "n"]
BISHOP = Literal["B", "b"]
QUEEN = Literal["Q", "q"]
KING = Literal["K", "k"]

PIECE = Literal[PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING]

p, r, n, b, q, k = Pawn, Rook, Knight, Bishop, Queen, King


# TODO import / export PGN !!(For testing)!!
# TODO test positions/scenarios
# TODO integrate stockfish (/alpha zero?)
# TODO import/export FEN

# TODO optimize _get_opponent_moves:
#   Cache pieces (with piece id), run before move + after to make sure move doesn't put king in check


class MoveStatus(Enum):
    VALID_SETUP = auto()
    VALID_MOVE = auto()

    INVALID_MOVE = auto()
    PUTS_KING_IN_CHECK = auto()

    KING_IN_CHECKMATE = auto()


class Board(dict):
    def __init__(self, _board_dict: dict[str, [Optional[Piece]]]):
        super().__init__(_board_dict)

    def to_fen(self):
        pass

    def to_pgn(self):
        pass

    def load_from_pgn(self):
        pass

    def load_from_fen(self):
        pass

    def set(self, key: str, value: Optional[Piece]) -> None:
        # move piece
        if isinstance(value, Piece):
            self[str(value.pos)] = None
            value.pos.set_with_notation(key)

        self[key] = value

    def display_ascii_board(self) -> None:
        _board = ["    a    b    c    d    e    f    g    h", "  " + "-" * 41]
        for y in range(1, 9):
            rank = f"{y} |"
            for x in range(1, 9):
                piece = self[f"{chr(x + 96)}{y}"]
                rank += f" {str(piece)}  |" if piece is not None else "    |"
            _board.append(rank)
            _board.append("  " + "-" * 41)

        _board.reverse()
        for row in _board:
            print(row)


class Game:
    def __init__(self, player_1: Player, player_2: Player):
        self.w_king = k(WHITE)
        self.b_king = k(BLACK)
        # set up board
        _b = {
            "a8": r(BLACK), "b8": n(BLACK), "c8": b(BLACK), "d8": q(BLACK), "e8": self.b_king, "f8": b(BLACK),
            "g8": n(BLACK), "h8": r(BLACK),
            "a7": p(BLACK), "b7": p(BLACK), "c7": p(BLACK), "d7": p(BLACK), "e7": p(BLACK), "f7": p(BLACK),
            "g7": p(BLACK), "h7": p(BLACK),
            "a6": None, "b6": None, "c6": None, "d6": None, "e6": None, "f6": None, "g6": None, "h6": None,
            "a5": None, "b5": None, "c5": None, "d5": None, "e5": None, "f5": None, "g5": None, "h5": None,
            "a4": None, "b4": None, "c4": None, "d4": None, "e4": None, "f4": None, "g4": None, "h4": None,
            "a3": None, "b3": None, "c3": None, "d3": None, "e3": None, "f3": None, "g3": None, "h3": None,
            "a2": p(WHITE), "b2": p(WHITE), "c2": p(WHITE), "d2": p(WHITE), "e2": p(WHITE), "f2": p(WHITE),
            "g2": p(WHITE), "h2": p(WHITE),
            "a1": r(WHITE), "b1": n(WHITE), "c1": b(WHITE), "d1": q(WHITE), "e1": self.w_king, "f1": b(WHITE),
            "g1": n(WHITE), "h1": r(WHITE)}
        self.board = Board(_b)

        for coord, piece in self.board.items():  # for calculation
            if piece is not None:
                piece.pos.set_with_notation(coord)

        # set up players
        # this can now be randomized easily
        self.players = {"WHITE": player_1, "BLACK": player_2}
        self.current_player = self.players["WHITE"]
        self.last_move = {"WHITE": {"piece": None, "pos": None},
                          "BLACK": {"piece": None, "pos": None}}

        # TODO is this easier?
        # self.current_piece
        # self.last_moved_piece

    @property
    def king_pos(self):
        return {"WHITE": self.w_king.pos, "BLACK": self.b_king.pos}

    def next_turn(self):
        self.current_player = self.players["WHITE"] if self.current_player.colour == BLACK else self.players["BLACK"]
        print(f"{self.current_player.name}'s turn!")

    def _check_if_legal_castle(self, side: str) -> bool:
        rank = 1 if self.current_player.colour == WHITE else 8
        opponent_moves = self._get_opponent_moves()

        if side == 'a':  # If queen-side castle
            if f"c{rank}" not in opponent_moves and f"d{rank}" not in opponent_moves:
                return True
        elif side == 'h':  # If king-side-castle
            if f"f{rank}" not in opponent_moves and f"g{rank}" not in opponent_moves:
                return True
        else:  # If not possible
            return False

    def _get_legal_pawn_moves(self, pawn: Pawn) -> list[BoardCoordinates]:
        legal_moves = []

        for move in pawn.move_atlas:
            try:
                if move == (0, 2) and pawn.pos.y not in (2, 7):
                    continue
                new_move = pawn.pos + move

                # check board
                piece_at_move = self.board.get(str(new_move))
                if piece_at_move is not None and piece_at_move.colour == self.current_player.colour:
                    continue
                elif piece_at_move is None and move in ((-1, 1), (1, 1)):
                    continue

                # check en passant
                opponent_colour = WHITE if self.current_player.colour == WHITE else BLACK

                last_move = self.last_move[opponent_colour]
                last_move_piece: Optional[Piece] = last_move["piece"]
                last_move_pos: Optional[BoardCoordinates] = last_move["pos"]

                if last_move_piece is not None and last_move_pos is not None:
                    long_step_rank = 4 if opponent_colour == WHITE else 5

                    if str(piece_at_move) == str(last_move_piece) and last_move_pos.x == long_step_rank:

                        if pawn.pos.x == last_move_pos.x + 1:
                            legal_moves.append(pawn.pos + (1, 1))

                        elif pawn.pos.x == last_move_pos.x - 1:
                            legal_moves.append(pawn.pos + (-1, 1))

                legal_moves.append(new_move)

            except InvalidPosition:
                pass

        return legal_moves

    def _get_opponent_moves(self, board: Board = None) -> list[str]:
        if board is None:
            board = self.board

        opponent_moves = []
        for _, piece in board.items():
            if piece is None:
                continue
            elif isinstance(piece, King):
                with suppress(InvalidPosition):
                    for move in piece.move_atlas:
                        new_pos = str(piece.pos + move)
                        piece_at_pos = self.board.get(new_pos)
                        if piece_at_pos is None or piece_at_pos.colour != self.current_player.colour:
                            opponent_moves.append(new_pos)


            else:
                if piece.colour != self.current_player.colour:
                    moves = self.get_legal_moves(piece)
                    [opponent_moves.append(str(move)) for move in moves]

        return opponent_moves

    def _get_legal_king_moves(self, king: King) -> dict[str, [Optional[list[BoardCoordinates]], dict[str, [bool]]]]:
        legal_moves = []
        a_castling, h_castling = False, False

        # check if castling possible
        if not king.has_moved:
            rank = 1 if self.current_player.colour == WHITE else 8
            back_rank = [self.board.get(f"{file}{rank}") for file in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')]
            possible_a_rook, possible_f_rook = back_rank[0], back_rank[7]
            try:
                if (
                        isinstance(back_rank[0], Rook)
                        and not possible_a_rook.has_moved
                        and all(piece is None for piece in back_rank[1:4])
                        and self._check_if_legal_castle(side='a')
                ):
                    a_castling = True
            except AttributeError:
                pass

            try:
                if (
                        isinstance(back_rank[7], Rook)
                        and not possible_f_rook.has_moved
                        and all(piece is None for piece in back_rank[5:7])
                        and self._check_if_legal_castle(side='h')
                ):
                    h_castling = True
            except AttributeError:
                pass

        legal_king_moves = []

        with suppress(InvalidPosition):
            for move in king.move_atlas:
                new_pos = king.pos + move
                piece_at_pos = self.board.get(new_pos)
                if piece_at_pos is None or piece_at_pos.colour == self.current_player.colour:
                    continue
                else:
                    legal_king_moves.append(move)

        opponent_moves = self._get_opponent_moves()

        if all(legal_move in opponent_moves for legal_move in legal_king_moves):
            legal_moves = None  # Checkmate
        else:
            for move in legal_king_moves:
                if move not in opponent_moves:
                    legal_moves.append(move)

        return {"legal_moves": legal_moves, "legal_castling": {"a": a_castling, "h": h_castling}}

    def get_legal_moves(self, piece: Piece) -> \
            Union[list[BoardCoordinates], dict[str, [list[BoardCoordinates], dict[str, str]]]]:
        # Doesn't check if player is in check

        legal_moves = []

        if isinstance(piece, Pawn):
            return self._get_legal_pawn_moves(piece)

        elif isinstance(piece, King):
            return self._get_legal_king_moves(piece)

        for move_x, move_y in piece.move_atlas:
            try:
                new_pos = piece.pos + BoardCoordinates(move_x, move_y)

            except InvalidPosition:
                continue

            if piece.can_make_long_move:
                while 1 <= new_pos.x + move_x <= 8 and 1 <= new_pos.y + move_y <= 8:  # check all possible spaces
                    new_pos.x += move_x
                    new_pos.y += move_y

                    new_pos_notation = str(new_pos)
                    piece_at_coord = self.board.get(new_pos_notation)

                    if piece_at_coord is not None:  # Stop checking for moves if piece is in the way
                        if piece_at_coord.colour != self.current_player.colour:  # if same colour ignore
                            legal_moves.append(new_pos_notation)
                        break

                    legal_moves.append(new_pos_notation)

            elif self.board[str(new_pos)] is not None and self.board[str(new_pos)].colour != self.current_player.colour:
                legal_moves.append(new_pos)

            elif self.board[str(new_pos)] is None:
                legal_moves.append(new_pos)

        return legal_moves

    def _set_up_move(self, piece: Piece, new_move_position: BoardCoordinates):
        current_pos = str(piece.pos)
        move_pos = str(new_move_position)
        legal_moves = self.get_legal_moves(piece)

        if new_move_position not in legal_moves:
            return MoveStatus.INVALID_MOVE, None, None

        temp_board = deepcopy(self.board)
        temp_board[current_pos] = None
        temp_board[move_pos] = piece

        if self.check_if_in_check(temp_board):
            return MoveStatus.PUTS_KING_IN_CHECK, None, None

        if isinstance(piece, King):
            return MoveStatus.VALID_SETUP, current_pos, move_pos, legal_moves

        return MoveStatus.VALID_SETUP, current_pos, move_pos

    def _make_pawn_move(self, piece: Pawn, new_move_position: BoardCoordinates) -> MoveStatus:
        move_status, current_pos, move_pos = self._set_up_move(piece, new_move_position)

        if move_status != MoveStatus.VALID_SETUP:
            return move_status

        if abs(piece.pos - new_move_position) == (1, 1):
            piece_at_board_pos = self.board.get(str(
                new_move_position - (0, 1) if self.current_player.colour == WHITE else new_move_position + (0, 1)
            ))
            self.current_player.captured_pieces.append(piece_at_board_pos)
            self.board.set(piece_at_board_pos.pos, None)

        self.board.set(current_pos, None)
        self.board.set(move_pos, piece)

    def _make_king_move(self, piece: King, new_move_position: BoardCoordinates) -> MoveStatus:
        move_status, current_pos, move_pos, legal_moves = self._set_up_move(piece, new_move_position)

        if move_status != MoveStatus.VALID_SETUP:
            return move_status

        piece_at_board_pos = self.board.get(move_pos)

        if new_move_position.x == 3 and legal_moves["legal_castling"]["a"]:
            # castle
            rank = 1 if self.current_player.colour == WHITE else 8

            rook = self.board.get(f"a{rank}")
            king = self.board.get(f"e{rank}")

            rook.pos.set_with_notation(f"d{rank}")
            king.pos.set_with_notation(f"c{rank}")

            self.board.set(f"d{rank}", rook)
            self.board.set(f"c{rank}", king)

        elif new_move_position.x == 7 and legal_moves["legal_castling"]["h"]:
            # castle
            rank = 1 if self.current_player.colour == WHITE else 8
            rook = self.board.get(f"h{rank}")
            king = self.board.get(f"e{rank}")

            self.board.set(f"f{rank}", rook)
            self.board.set(f"g{rank}", king)

        elif piece_at_board_pos is None:
            self.board.set(move_pos, piece)
            self.board[current_pos] = None

        elif piece_at_board_pos.colour != self.current_player.colour:
            self.current_player.captured_pieces.append(piece_at_board_pos)
            self.board.set(move_pos, piece)
            self.board[current_pos] = None

        if not piece.has_moved:
            piece.has_moved = True

        return MoveStatus.VALID_MOVE

    def make_move(self, piece: Piece, new_move_position: BoardCoordinates) -> MoveStatus:
        """ Returns a bool based on if the move was successful or not"""
        if isinstance(piece, Pawn):
            return self._make_pawn_move(piece, new_move_position)

        elif isinstance(piece, King):
            return self._make_king_move(piece, new_move_position)

        current_pos = str(piece.pos)
        move_pos = str(new_move_position)
        legal_moves = self.get_legal_moves(piece)

        if new_move_position not in legal_moves:
            return MoveStatus.INVALID_MOVE  # Illegal, illegal move

        temp_board = deepcopy(self.board)

        temp_board[move_pos] = piece
        temp_board[current_pos] = None

        if self.check_if_in_check(temp_board):
            return MoveStatus.PUTS_KING_IN_CHECK  # Illegal, move puts player in check

        piece_at_board_pos = self.board.get(move_pos)

        try:
            if piece_at_board_pos.colour != self.current_player.colour:
                self.current_player.captured_pieces.append(piece_at_board_pos)

        except AttributeError:
            pass

        self.board.set(move_pos, piece)
        self.board.set(current_pos, None)

        if isinstance(piece, Rook) and not piece.has_moved:
            piece.has_moved = True

        return MoveStatus.VALID_MOVE

    def check_if_in_check(self, board: Optional[Board] = None) -> bool:
        if board is None:
            board = self.board

        return self.king_pos[self.current_player.colour] in self._get_opponent_moves(board)



class Player:
    name: str
    game: Game
    hasMoved: bool
    captured_pieces = []

    def __init__(self, name, colour):
        self.in_check = False
        self.name, self.colour, self.hasMoved = name, colour, False
