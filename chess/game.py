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

ID = int


# TODO notify user when king in check
# TODO implement halfmove clock
# TODO implement move count
# TODO implement repetition rules (should be 'fairly' straightforward as moves need to be logged anyways
#      (might have difficulty with pattern rec)

# TODO import / export PGN
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
    DRAW = auto()


class Board(dict):
    def __init__(self, _board_dict: dict[str, [Optional[Piece]]]):
        super().__init__(_board_dict)

    @property
    def _fen(self):
        return {"rank_1": "",
                "rank_2": "",
                "rank_3": "",
                "rank_4": "",
                "rank_5": "",
                "rank_6": "",
                "rank_7": "",
                "rank_8": "",
                "last_to_move": "",
                "castling_rights": "-",
                "en_passant_target": "-",
                "halfmove_clock": "0",
                "fullmove_counter": "0"
                }

    def to_fen(self, game: Game):
        # TODO half/fullmove counter
        fen = self._fen

        # Piece placement
        rank_counter = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0}
        for pos, piece in self.items():
            if piece is not None:
                rank = f"rank_{pos[1]}"
                if rank_counter[pos[1]] != 0:
                    fen[rank] += str(rank_counter[pos[1]])
                fen[rank] += str(piece)
                rank_counter[pos[1]] = 0
            else:
                rank_counter[pos[1]] += 1

        for rank, count in rank_counter.items():
            if count != 0:
                fen[f"rank_{rank}"] += str(count)

        # Castling rights
        castling_rights = ""
        possible_white_h_rook = game.board.get("h1")
        possible_white_a_rook = game.board.get("a1")
        possible_black_h_rook = game.board.get("h8")
        possible_black_a_rook = game.board.get("a8")

        if not game.w_king.has_moved:
            if possible_white_h_rook is not None and not possible_white_h_rook.has_moved:
                castling_rights += "K"
            if possible_white_a_rook is not None and not possible_white_a_rook.has_moved:
                castling_rights += "Q"
        if not game.b_king.has_moved:
            if possible_black_h_rook is not None and not possible_black_h_rook.has_moved:
                castling_rights += "k"
            if possible_black_a_rook is not None and not possible_black_a_rook.has_moved:
                castling_rights += "q"

        fen["castling_rights"] = castling_rights

        # FEN assembly
        # ei: rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2
        final_fen = "".join(fen[f"rank_{rank}"] + "/" for rank in range(8, 1, -1))
        final_fen += fen[f"rank_{1}"]
        final_fen += " " + "w" if game.current_player.colour == WHITE else "b"
        final_fen += " " + fen["castling_rights"]
        final_fen += " " + fen["en_passant_target"]
        final_fen += " " + fen["halfmove_clock"]
        final_fen += " " + fen["fullmove_counter"]

        print(final_fen)

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

    def move(self, piece: Piece, move_pos: BoardCoordinates) -> None:
        self[str(piece.pos)] = None
        self[str(move_pos)] = piece

        piece.pos = move_pos

    def take(self, piece: Piece) -> None:
        self[str(piece.pos)] = None

    def to_ascii(self) -> list[str]:
        board = ["    a    b    c    d    e    f    g    h", "  " + "-" * 41]
        for y in range(1, 9):
            rank = f"{y} |"
            for x in range(1, 9):
                piece = self[f"{chr(x + 96)}{y}"]
                rank += f" {str(piece)}  |" if piece is not None else "    |"
            board.append(rank)
            board.append("  " + "-" * 41)
        board.reverse()
        return board


class Game:
    en_passant_target: Optional[Pawn] = None
    players: dict[piece_colour, Player] = {}

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
            "g1": n(WHITE), "h1": r(WHITE)
        }
        self.board = Board(_b)

        self._pieces = {}
        for coord, piece in self.board.items():  # for calculation
            if piece is not None:
                piece.pos.set_with_notation(coord)
                # set send pieces to own dict to prevent having to iterate over the entire board
                # id not used but needed to differentiate between instances

                self._pieces[(str(piece), id(piece))] = piece

        # set up players

        for player in (player_1, player_2):
            self.players[player.colour] = player

        self.current_player = self.players[WHITE]

        self.past_positions = []

    @property
    def player_colour(self):
        return self.current_player.colour

    @property
    def opponent_colour(self):
        return WHITE if self.player_colour == BLACK else WHITE

    @property
    def king_pos(self):
        return {"WHITE": self.w_king.pos, "BLACK": self.b_king.pos}

    @staticmethod
    def _remove_duplicates(array: list[BoardCoordinates]) -> list[BoardCoordinates]:
        # TODO is this needed?
        temp = []
        for coord in array:
            if coord not in temp:
                temp.append(coord)
        return temp

    def next_turn(self):
        self.current_player = self.players[WHITE] if self.player_colour == BLACK else self.players[BLACK]
        print(f"{self.current_player.name}'s turn!")

    def get_pieces(self, colour: Optional[Colour]) -> dict[tuple[str, ID], Piece]:
        pieces = {}

        if colour is None:
            pieces = self._pieces

        elif colour == BLACK:
            for piece_id, piece in self._pieces.items():
                if piece_id[0].islower() and colour == BLACK:
                    pieces[piece_id] = piece
                elif piece_id[0].isupper() and colour == WHITE:
                    pieces[piece_id] = piece

        return pieces

    def move_piece(self, piece: Piece, new_move_pos: BoardCoordinates):
        self.board.move(piece, new_move_pos)

    def take_piece(self, piece: Piece):
        self.board.take(piece)
        self.current_player.captured_pieces.append(piece)

    def move_puts_king_in_check(self, piece: Piece, move_pos: BoardCoordinates) -> bool:
        temp_board = deepcopy(self.board)
        temp_board.move(piece, move_pos)

        return self.check_if_in_check(temp_board)

    def check_if_in_check(self, board: Optional[Board] = None) -> bool:
        if board is None:
            board = self.board

        return self.king_pos[self.player_colour] in self._get_opponent_moves(board)

    def threefold_repetition(self) -> bool:
        self.past_positions.append(self.board.to_ascii())
        return self.past_positions.count(self.board.to_ascii()) >= 3  # >= isn't necessary - for safety

    def get_legal_moves(self, piece: Piece) -> \
            Union[list[BoardCoordinates], dict[str, [list[BoardCoordinates], dict[str, str]]]]:
        # Doesn't check if player is in check

        legal_moves = []

        if isinstance(piece, Pawn):
            return self._get_legal_pawn_moves(piece)

        elif isinstance(piece, King):
            return self._get_legal_king_moves(piece)

        for coord in piece.move_atlas:

            if piece.can_make_long_move:
                new_pos = piece.pos

                with suppress(InvalidPosition):
                    while True:  # check all possible spaces
                        new_pos += coord
                        piece_at_coord = self.board.get(str(new_pos))

                        if piece_at_coord is not None:  # Stop checking for moves if piece is in the way
                            if (
                                    piece_at_coord.colour == self.opponent_colour
                                    and not self.move_puts_king_in_check(piece, new_pos)
                            ):
                                legal_moves.append(new_pos)
                            break

                        if not self.move_puts_king_in_check(piece, new_pos):
                            legal_moves.append(new_pos)
                            continue

            else:

                try:
                    new_pos = piece.pos + coord

                except InvalidPosition:
                    continue

            piece_at_pos = self.board[str(new_pos)]

            if piece_at_pos is not None or piece_at_pos == self.opponent_colour:
                legal_moves.append(new_pos)

            else:
                continue

        return legal_moves

    def _get_legal_pawn_moves(self, pawn: Pawn) -> list[BoardCoordinates]:
        legal_moves = []

        for move in pawn.move_atlas:
            try:
                if abs(move) == (0, 2) and pawn.has_moved:
                    continue

                try:
                    move_pos = pawn.pos + move

                except InvalidPosition:
                    continue

                # check board
                piece_at_move = self.board.get(str(move_pos))

                if abs(move) == (1, 1):

                    # check if pawn takes piece
                    if piece_at_move is not None and piece_at_move.colour == self.opponent_colour:
                        legal_moves.append(move_pos)

                    # check if en passant target exists
                    elif isinstance(self.en_passant_target, Pawn):
                        # TODO this can probably be cleaned up
                        with suppress(InvalidPosition):
                            if self.en_passant_target.pos == pawn.pos + (-1, 0):
                                legal_moves.append(pawn.pos + (-1, 1) if pawn.colour == WHITE else pawn.pos + (-1, -1))

                        with suppress(InvalidPosition):
                            if self.en_passant_target.pos == pawn.pos + (1, 0):
                                legal_moves.append(pawn.pos + (1, 1) if pawn.colour == WHITE else pawn.pos + (1, -1))

                elif piece_at_move is None and not self.move_puts_king_in_check(pawn, move_pos):
                    legal_moves.append(move_pos)

            except InvalidPosition:
                continue

        return self._remove_duplicates(legal_moves)

    def _get_legal_king_moves(self, king: King) -> dict[str, [Optional[list[BoardCoordinates]], dict[str, [bool]]]]:
        legal_moves = []
        a_castling, h_castling = False, False

        # check if castling possible
        if not king.has_moved:
            rank = 1 if self.player_colour == WHITE else 8
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

        with suppress(InvalidPosition):
            for move in king.move_atlas:
                new_pos = king.pos + move
                piece_at_pos = self.board.get(str(new_pos))

                if piece_at_pos is not None and piece_at_pos.colour == self.player_colour:
                    continue

                else:
                    legal_moves.append(new_pos)

        opponent_moves = self._get_opponent_moves()

        if all(legal_move in opponent_moves for legal_move in legal_moves):
            legal_moves = None  # Possible Checkmate
        print(f"{legal_moves = }, {king.pos = }, {opponent_moves = }")
        return {"legal_moves": legal_moves, "legal_castling": {"a": a_castling, "h": h_castling}}

    def _check_if_legal_castle(self, side: str) -> bool:
        rank = 1 if self.player_colour == WHITE else 8
        opponent_moves = self._get_opponent_moves()

        if side == 'a':  # If queen-side castle
            if f"c{rank}" not in opponent_moves and f"d{rank}" not in opponent_moves:
                return True
        elif side == 'h':  # If king-side-castle
            if f"f{rank}" not in opponent_moves and f"g{rank}" not in opponent_moves:
                return True
        else:  # If not possible
            return False

    def make_move(self, piece: Piece, new_move_position: BoardCoordinates) -> MoveStatus:
        print(f"{piece = }, {piece.pos = }")
        """ Returns a bool based on if the move was successful or not"""
        if isinstance(piece, Pawn):
            return self._make_pawn_move(piece, new_move_position)
        else:
            self.en_passant_target = None

        if isinstance(piece, King):
            return self._make_king_move(piece, new_move_position)

        current_pos = str(piece.pos)
        move_pos = str(new_move_position)
        legal_moves = self.get_legal_moves(piece)

        if new_move_position not in legal_moves:
            print(f"{new_move_position = }, {legal_moves = }")
            return MoveStatus.INVALID_MOVE  # Illegal, illegal move

        temp_board = deepcopy(self.board)

        temp_board[move_pos] = piece
        temp_board[current_pos] = None

        if self.check_if_in_check(temp_board):
            return MoveStatus.PUTS_KING_IN_CHECK  # Illegal, move puts player in check

        piece_at_board_pos = self.board.get(move_pos)

        try:
            if piece_at_board_pos.colour == self.opponent_colour:
                self.current_player.captured_pieces.append(piece_at_board_pos)

        except AttributeError:
            pass

        self.board.set(move_pos, piece)
        self.board.set(current_pos, None)

        if isinstance(piece, Rook) and not piece.has_moved:
            piece.has_moved = True

        return MoveStatus.VALID_MOVE

    def _set_up_move(self, piece: Piece, new_move_position: BoardCoordinates):
        current_pos = str(piece.pos)
        move_pos = str(new_move_position)
        legal_moves = self.get_legal_moves(piece)
        invalid_move = False

        if (
                isinstance(legal_moves, dict)
                and legal_moves["legal_moves"] is not None
                and new_move_position not in legal_moves["legal_moves"]
        ):
            invalid_move = True

        elif (
                isinstance(legal_moves, dict)
                and legal_moves["legal_moves"] is None
                and not legal_moves["legal_castling"]["a"]
                and not legal_moves["legal_castling"]["h"]
        ):
            invalid_move = True

        elif not isinstance(legal_moves, dict) and new_move_position not in legal_moves:
            invalid_move = True

        if invalid_move:
            if isinstance(piece, King):
                return MoveStatus.INVALID_MOVE, None, None, None
            return MoveStatus.INVALID_MOVE, None, None

        temp_board = deepcopy(self.board)
        temp_board[current_pos] = None
        temp_board[move_pos] = piece

        if self.check_if_in_check(temp_board):
            return MoveStatus.PUTS_KING_IN_CHECK, None, None

        if isinstance(piece, King):
            return MoveStatus.VALID_SETUP, current_pos, move_pos, legal_moves

        return MoveStatus.VALID_SETUP, current_pos, move_pos

    def _make_pawn_move(self, pawn: Pawn, new_move_position: BoardCoordinates) -> MoveStatus:
        move_status, current_pos, move_pos = self._set_up_move(pawn, new_move_position)

        if move_status != MoveStatus.VALID_SETUP:
            return move_status

        if abs(pawn.pos - new_move_position) == (1, 1):

            # check if move is to take at |(1, 1)|
            piece_at_board_pos = self.board.get(str(new_move_position))

            # if not, get en passant targets
            if piece_at_board_pos is None:

                with suppress(InvalidPosition):
                    if self.en_passant_target == str(pawn.pos + (-1, 0)):
                        piece_at_board_pos = self.board.get(str(pawn.pos + (-1, 0)))

                with suppress(InvalidPosition):
                    if self.en_passant_target == str(pawn.pos + (1, 0)):
                        piece_at_board_pos = self.board.get(str(pawn.pos + (1, 0)))

            self.take_piece(piece_at_board_pos)

        if abs(pawn.pos - new_move_position) in ((0, -2), (0, 2)):

            try:
                if self.player_colour == WHITE:
                    self.en_passant_target = pawn.pos + (0, 2)

            except InvalidPosition:
                pass

            try:
                if self.player_colour == BLACK:
                    self.en_passant_target = pawn.pos + (0, -2)

            except InvalidPosition:
                pass

            pawn.has_moved = True

        self.board.set(current_pos, None)
        self.board.set(move_pos, pawn)

        return MoveStatus.VALID_MOVE

    def _make_king_move(self, piece: King, new_move_position: BoardCoordinates) -> MoveStatus:
        move_status, current_pos, move_pos, legal_moves = self._set_up_move(piece, new_move_position)

        if move_status != MoveStatus.VALID_SETUP:
            return move_status

        piece_at_board_pos = self.board.get(move_pos)

        if new_move_position.x == 3 and legal_moves["legal_castling"]["a"]:
            # castle
            rank = 1 if self.player_colour == WHITE else 8

            rook = self.board.get(f"a{rank}")
            king = self.board.get(f"e{rank}")

            rook.pos.set_with_notation(f"d{rank}")
            king.pos.set_with_notation(f"c{rank}")

            self.board.set(f"d{rank}", rook)
            self.board.set(f"c{rank}", king)

        elif new_move_position.x == 7 and legal_moves["legal_castling"]["h"]:
            # castle
            rank = 1 if self.player_colour == WHITE else 8
            rook = self.board.get(f"h{rank}")
            king = self.board.get(f"e{rank}")

            self.board.set(f"f{rank}", rook)
            self.board.set(f"g{rank}", king)

        elif piece_at_board_pos is None:
            self.board.set(move_pos, piece)
            self.board[current_pos] = None

        elif piece_at_board_pos.colour == self.opponent_colour:
            self.current_player.captured_pieces.append(piece_at_board_pos)
            self.board.set(move_pos, piece)
            self.board[current_pos] = None

        if not piece.has_moved:
            piece.has_moved = True

        return MoveStatus.VALID_MOVE

    def _get_opponent_moves(self, board: Board = None) -> list[BoardCoordinates]:
        # TODO this is royally fucked
        if board is None:
            board = self.board

        pieces = self.get_pieces(self.opponent_colour)

        opponent_moves = []
        for _, piece in pieces.items():

            if isinstance(piece, King):
                return self._get_legal_opponent_king_moves(piece, board)

            elif isinstance(piece, Pawn):
                return self._get_legal_opponent_pawn_moves(piece, board)

            else:
                for move in piece.move_atlas:
                    with suppress(InvalidPosition):
                        new_pos = piece.pos + move
                        piece_at_pos = board.get(str(new_pos))

                        if piece_at_pos is not None and piece_at_pos.colour == self.opponent_colour:
                            continue

                        elif piece.can_make_long_move:
                            new_pos = piece.pos

                            with suppress(InvalidPosition):
                                while True:
                                    new_pos += move
                                    piece_at_pos = self.board.get(str(new_pos))

                                    if piece_at_pos is not None:  # Stop checking for moves if piece is in the way

                                        if piece_at_pos.colour == self.opponent_colour:
                                            opponent_moves.append(new_pos)

                                        break

                                    if not self.move_puts_king_in_check(piece, new_pos):
                                        opponent_moves.append(new_pos)
                                        continue
                        else:
                            try:
                                new_pos = piece.pos + move
                            except InvalidPosition:
                                continue

                            piece_at_pos = self.board[str(new_pos)]

                            if piece_at_pos is not None or piece_at_pos == self.player_colour:
                                opponent_moves.append(new_pos)

                            else:
                                continue

        return opponent_moves

    def _get_legal_opponent_pawn_moves(self, pawn: Pawn, board: Board = None) -> list[BoardCoordinates]:
        opponent_moves = []
        for move in pawn.move_atlas:
            with suppress(InvalidPosition):
                new_pos = pawn.pos + move
                piece_at_pos = board.get(str(new_pos))

                if abs(move) == (0, 2) and pawn.has_moved:
                    continue

                elif (
                        abs(move) == (1, 1)
                        and (piece_at_pos is None or piece_at_pos.colour == self.opponent_colour)
                ):
                    continue

                elif piece_at_pos is not None:
                    continue

                else:
                    opponent_moves.append(new_pos)

        return opponent_moves

    def _get_legal_opponent_king_moves(self, king: King, board: Board) -> list[BoardCoordinates]:
        opponent_moves = []
        for move in king.move_atlas:
            with suppress(InvalidPosition):
                new_pos = king.pos + move
                piece_at_pos = board.get(str(new_pos))

                if piece_at_pos is not None and piece_at_pos.colour == self.player_colour:
                    opponent_moves.append(new_pos)

        return opponent_moves


class Player:
    name: str
    game: Game
    hasMoved: bool
    captured_pieces = []

    def __init__(self, name, colour):
        self.in_check = False
        self.name, self.colour, self.hasMoved = name, colour, False
