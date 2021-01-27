WHITE, BLACK, EMPTY = "WHITE", "BLACK", "EMPTY"

class Game:
    pieces: []
    deadPieces: []
    def __init__(self):
        self.pieces = [Rook(0, 0, BLACK, self), Knight(1, 0, BLACK, self), Bishop(2, 0, BLACK, self), Queen(3, 0, BLACK, self), King(4, 0, BLACK, self), Bishop(5, 0, BLACK, self), Knight(6, 0, BLACK, self), Rook(7, 0, BLACK, self),
                       Pawn(0, 1, BLACK, self), Pawn(1, 1, BLACK, self), Pawn(2, 1, BLACK, self), Pawn(3, 1, BLACK, self), Pawn(4, 1, BLACK, self), Pawn(5, 1, BLACK, self), Pawn(6, 1, BLACK, self), Pawn(7, 1, BLACK, self),
                       Pawn(0, 6, WHITE, self), Pawn(1, 6, WHITE, self), Pawn(2, 6, WHITE, self), Pawn(3, 6, WHITE, self), Pawn(4, 6, WHITE, self), Pawn(5, 6, WHITE, self), Pawn(6, 6, WHITE, self), Pawn(7, 6, WHITE, self),
                       Rook(0, 7, WHITE, self), Knight(1, 7, WHITE, self), Bishop(2, 7, WHITE, self), Queen(3, 7, WHITE, self), King(4, 7, WHITE, self), Bishop(5, 7, WHITE, self), Knight(6, 7, WHITE, self), Rook(7, 7, WHITE, self)]

    def getEmptySpaces(self):
        empty = [[i, j] for j in range(8) for i in range(8)]
        for piece in self.pieces:
            pos = [piece.x, piece.y]
            if pos in empty:
                empty.remove(pos)
        return empty
    
    def getXY(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return EMPTY

class Piece:
    x: int
    y: int
    colour: str
    game: Game
    def __init__(self, x, y, colour, game):
        self.x, self.y, self.colour, self.game = x, y, colour, game

    def toString(self):
        return f"{self.colour} {type(self)} on ({self.x}, {self.y})."

class Pawn(Piece):
    def getAvailableMoves(self):
        moves = []
        if (self.colour == BLACK):
            movesToCheck = [[self.x + 1, self.y],
                            [self.x + 1, self.y + 1],
                            [self.x + 1, self.y - 1]]
            x = [self.game.getXY(x, y) for x, y in movesToCheck]

            if self.x == 1:
                pass # check for 2 spaces on first move
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