from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Union, Optional


# Consts
WHITE, BLACK = "WHITE", "BLACK"

# Typing
Colour = Literal["WHITE", "BLACK"]


@dataclass
class BoardCoordinates:
    """ (x, y) position of the board

        [0 indexed coordinates for cleaner indexing]


        Container class for (x, y) coordinates of the board.
        a - h  =  0 - 7
        1 - 8  =  0 - 7

              a        b        c        d        e        f        g        h
        8  (1, 8)   (2, 8)   (3, 8)   (4, 8)   (5, 8)   (6, 8)   (7, 8)   (8, 8)\n
        7  (1, 7)   (2, 7)   (3, 7)   (4, 7)   (5, 7)   (6, 7)   (7, 7)   (8, 7)\n
        6  (1, 6)   (2, 6)   (3, 6)   (4, 6)   (5, 6)   (6, 6)   (7, 6)   (8, 6)\n
        5  (1, 5)   (2, 5)   (3, 5)   (4, 5)   (5, 5)   (6, 5)   (7, 5)   (8, 5)\n
        4  (1, 4)   (2, 4)   (3, 4)   (4, 4)   (5, 4)   (6, 4)   (7, 4)   (8, 4)\n
        3  (1, 3)   (2, 3)   (3, 3)   (4, 3)   (5, 3)   (6, 3)   (7, 3)   (8, 3)\n
        2  (1, 2)   (2, 2)   (3, 2)   (4, 2)   (5, 2)   (6, 2)   (7, 2)   (8, 2)\n
        1  (1, 1)   (2, 1)   (3, 1)   (4, 1)   (5, 1)   (6, 1)   (7, 1)   (8, 1)\n

    """

    x: int
    y: int

    def __eq__(self, other: Union[BoardCoordinates, str]):
        if isinstance(other, str):  # not sure where this is taking place but is needed to fix this garbage
            return str(self) == other
        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]

        return self.x == other.x and self.y == other.y

    def __add__(self, other: Union[tuple[int, int], BoardCoordinates]):
        if isinstance(other, tuple):
            return BoardCoordinates(*self.check_bounds(self.x + other[0], self.y + other[1]))

        elif isinstance(other, BoardCoordinates):
            return BoardCoordinates(*self.check_bounds(self.x + other.x, self.y + other.y))

        else:
            raise NotImplemented

    def __sub__(self, other: Union[tuple[int, int], BoardCoordinates]):  # bounds check not needed (only used for calc)
        if isinstance(other, tuple):
            return BoardCoordinates(self.x - other[0], self.y - other[1])

        elif isinstance(other, BoardCoordinates):
            return BoardCoordinates(self.x - other.x, self.y - other.y)

        else:
            raise NotImplemented

    def __abs__(self):
        return abs(self.x), abs(self.y)

    def __str__(self):
        return self.get_notation()

    def set_with_xy(self, coordinates: Union[tuple[int, int], list[int, int]]) -> None:
        self.x, self.y = self.check_bounds(coordinates)

    def get_xy(self) -> list[int, int]:  # Not a tuple to allow coord mutation
        return [self.x, self.y]

    def set_with_notation(self, coordinate: str) -> None:

        # Sanity check
        if len(coordinate) != 2:
            raise InvalidPosition(coordinate)

        # Try conversion + assignment
        try:
            self.x, self.y = self.check_bounds(ord(coordinate[0]) - 96, int(coordinate[1]))

        except (TypeError, InvalidPosition):
            raise InvalidPosition(coordinate)

    def get_notation(self) -> str:
        return chr(96 + self.x) + str(self.y)

    def check_bounds(self, *coordinate) -> Optional[Union[tuple[int, int], BoardCoordinates]]:
        try:

            coordinate = coordinate[0] if isinstance(coordinate[0], (list, tuple, BoardCoordinates)) else coordinate

        except IndexError:

            if self.x < 1 or self.x > 8 or self.y < 1 or self.y > 8:
                raise InvalidPosition(self)

            return None

        if isinstance(coordinate, (list, tuple)):

            if coordinate[0] < 1 or coordinate[0] > 8 or coordinate[1] < 1 or coordinate[1] > 8:
                raise InvalidPosition(coordinate)

            return coordinate

        elif isinstance(coordinate, BoardCoordinates):

            if coordinate.x < 1 or coordinate.x > 8 or coordinate.y < 1 or coordinate.y > 8:
                raise InvalidPosition(coordinate)

            return coordinate


class InvalidPosition(Exception):
    def __init__(self, position: Union[str, list[int, int], tuple, BoardCoordinates]):
        if isinstance(position, (list, tuple)):
            position = f"({position[0]}, {position[1]})"

        elif isinstance(position, BoardCoordinates):
            position = str(position)

        super().__init__(f"Invalid position received: {position}")


class Piece:
    pos: BoardCoordinates
    colour: Colour
    move_atlas: list[BoardCoordinates]
    can_make_long_move: bool

    def __init__(self):
        self.pos = BoardCoordinates(-1, -1)  # init with invalid pos


class Pawn(Piece):
    move_atlas = [BoardCoordinates(0, 1),
                  BoardCoordinates(0, 2),
                  BoardCoordinates(1, 1),
                  BoardCoordinates(-1, 1)]
    can_make_long_move = False
    has_moved = False
    atlas_was_flipped = False

    def __init__(self, colour: Colour):
        self.colour = colour
        super().__init__()

        if self.colour == BLACK:
            temp = []
            for move in self.move_atlas:
                move = BoardCoordinates(move.x, -move.y)
                temp.append(move)
            self.move_atlas = temp

    def __str__(self):
        return 'P' if self.colour == WHITE else 'p'


class Rook(Piece):
    move_atlas = [BoardCoordinates(0, 1),
                  BoardCoordinates(0, -1),
                  BoardCoordinates(1, 0),
                  BoardCoordinates(-1, 0)]
    can_make_long_move = True
    has_moved = False

    def __init__(self, colour: Colour):
        self.colour = colour
        super().__init__()

    def __str__(self):
        return 'R' if self.colour == WHITE else 'r'


class Knight(Piece):
    move_atlas = [BoardCoordinates(2, 1),
                  BoardCoordinates(2, -1),
                  BoardCoordinates(-2, 1),
                  BoardCoordinates(-2, -1),
                  BoardCoordinates(1, 2),
                  BoardCoordinates(1, -2),
                  BoardCoordinates(-1, 2),
                  BoardCoordinates(-1, -2)]
    can_make_long_move = False

    def __init__(self, colour: Colour):
        self.colour = colour
        super().__init__()

    def __str__(self):
        return 'N' if self.colour == WHITE else 'n'


class Bishop(Piece):
    move_atlas = [BoardCoordinates(1, 1),
                  BoardCoordinates(-1, 1),
                  BoardCoordinates(-1, -1),
                  BoardCoordinates(1, -1)]

    can_make_long_move = True

    def __init__(self, colour: Colour):
        self.colour = colour
        super().__init__()

    def __str__(self):
        return 'B' if self.colour == WHITE else 'b'


class Queen(Piece):
    move_atlas = [BoardCoordinates(0, 1),
                  BoardCoordinates(0, -1),
                  BoardCoordinates(1, 0),
                  BoardCoordinates(-1, 0),
                  BoardCoordinates(1, 1),
                  BoardCoordinates(1, -1),
                  BoardCoordinates(-1, 1),
                  BoardCoordinates(-1, -1)]

    can_make_long_move = True

    def __init__(self, colour: Colour):
        self.colour = colour
        super().__init__()

    def __str__(self):
        return 'Q' if self.colour == WHITE else 'q'


class King(Piece):
    move_atlas = [BoardCoordinates(0, 1),
                  BoardCoordinates(0, -1),
                  BoardCoordinates(1, 0),
                  BoardCoordinates(-1, 0),
                  BoardCoordinates(1, 1),
                  BoardCoordinates(1, -1),
                  BoardCoordinates(-1, 1),
                  BoardCoordinates(-1, -1)]

    can_make_long_move = False
    has_moved = False

    def __init__(self, colour: Colour):
        self.colour = colour
        super().__init__()

    def __str__(self):
        return 'K' if self.colour == WHITE else 'k'
