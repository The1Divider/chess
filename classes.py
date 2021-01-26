WHITE, BLACK, EMPTY = "WHITE", "BLACK", "EMPTY"

class Game:
    pieces: []
    def __init__(self):
        self.pieces = [Rook(0, 0, BLACK), Knight(1, 0, BLACK), Bishop(2, 0, BLACK), Queen(3, 0, BLACK), King(4, 0, BLACK), Bishop(5, 0, BLACK), Knight(6, 0, BLACK), Rook(7, 0, BLACK), Pawn(0, 1, BLACK), Pawn(1, 1, BLACK), Pawn(2, 1, BLACK), Pawn(3, 1, BLACK), Pawn(4, 1, BLACK), Pawn(5, 1, BLACK), Pawn(6, 1, BLACK), Pawn(7, 1, BLACK), Pawn(0, 6, WHITE), Pawn(1, 6, WHITE), Pawn(2, 6, WHITE), Pawn(3, 6, WHITE), Pawn(4, 6, WHITE), Pawn(5, 6, WHITE), Pawn(6, 6, WHITE), Pawn(7, 6, WHITE), Rook(0, 7, WHITE), Knight(1, 7, WHITE), Bishop(2, 7, WHITE), Queen(3, 7, WHITE), King(4, 7, WHITE), Bishop(5, 7, WHITE), Knight(6, 7, WHITE), Rook(7, 7, WHITE)]

    def getEmptySpaces(self):
        empty = [[i, j] for j in range(8) for i in range(8)]
        for piece in self.pieces:
            pos = [piece.x, piece.y]
            if pos in empty:
                empty.remove(pos)
        return empty
    
    def getXY(self, x, y):
        status = EMPTY
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                status = piece
        return status

class Piece:
    x: int
    y: int
    colour: str
    def __init__(self, x, y, colour):
        self.x, self.y, self.colour = x, y, colour

    def toString(self):
        return f"{self.colour} {type(self)} on ({self.x}, {self.y})."

class Pawn(Piece):
    def getAvailableMoves():
        moves = []
        if (self.colour == BLACK):
            pass
        else:
            pass
        return moves

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass