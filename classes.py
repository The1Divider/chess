WHITE, BLACK, EMPTY = "WHITE", "BLACK", "EMPTY"

class Game:
    pieces: []
    deadPieces: []
    def __init__(self):
        self.pieces = [Rook(0, 0, BLACK, self), Knight(1, 0, BLACK, self), Bishop(2, 0, BLACK, self), Queen(3, 0, BLACK, self), King(4, 0, BLACK, self), Bishop(5, 0, BLACK, self), Knight(6, 0, BLACK, self), Rook(7, 0, BLACK, self),
                       Pawn(0, 1, BLACK, self), Pawn(1, 1, BLACK, self), Pawn(2, 1, BLACK, self), Pawn(3, 1, BLACK, self), Pawn(4, 1, BLACK, self), Pawn(5, 1, BLACK, self), Pawn(6, 1, BLACK, self), Pawn(7, 1, BLACK, self),
                       #Pawn(0, 6, WHITE, self), Pawn(1, 6, WHITE, self), Pawn(2, 6, WHITE, self), Pawn(3, 6, WHITE, self), Pawn(4, 6, WHITE, self), Pawn(5, 6, WHITE, self), Pawn(6, 6, WHITE, self), Pawn(7, 6, WHITE, self),
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
        return None

class Piece:
    x: int
    y: int
    colour: str
    hasMoved: bool
    directions: []
    game: Game
    def __init__(self, x, y, colour, game):
        self.x, self.y, self.colour, self.game = x, y, colour, game
        self.hasMoved = False
    
    def checkIllegalMoves(self, moves):
        for x, y in moves:
            if x > 7 or x < 0 or y > 7 or y < 0:
                moves.remove([x, y])
        return moves
    
    def getAvailableMoves(self, canGoFar):
        moves = []
        if canGoFar:
            for xAdd, yAdd in self.directions:
                count = 1
                x, y = self.x + count * xAdd, self.y + count * yAdd
                while x < 8 and x > -1 and y < 8 and y > -1 and self.game.getXY(x, y) == None:      # While x, y in bounds of the board and the square is empty, add to moves
                    moves.append([x, y])
                    count += 1
                    x, y = self.x + count * xAdd, self.y + count * yAdd
                if self.game.getXY(x, y) != None and self.game.getXY(x, y).colour != self.colour:   # Once all empty squares are taken care of, if enemy player is on tile, add to moves
                    moves.append([x, y])
        else:
            for xAdd, yAdd in self.directions:
                x, y = self.x + xAdd, self.y + yAdd
                if x < 8 and x > -1 and y < 8 and y > -1 and (self.game.getXY(x, y) == None or self.game.getXY(x, y).colour != self.colour):    # if x, y in bounds of board and square is either empty or contains an enemy
                    moves.append([x, y])
        return moves

    def toString(self):
        return f"{self.colour} {type(self)} on ({self.x}, {self.y})."

class Pawn(Piece):
    def getAvailableMoves(self):
        moves = []
        direction = 1 if self.colour == BLACK else -1
        # if the space ahead of the pawn is empty, allow the pawn to move ahead
        if self.game.getXY(self.x, self.y + direction) == None:
            moves.append([self.x, self.y + direction])
        # if the squares ahead one and diagonal to the pawn has an enemy piece on it, allow the move
        for x, y in [[self.x + 1, self.y + direction], [self.x - 1, self.y + direction]]:
            if self.game.getXY(x, y) != None and self.game.getXY(x, y).colour != self.colour:
                moves.append([x, y])
        # if y + 1 and y + 2 is empty and the pawn hasn't moved yet, allow it to move further on its first turn
        if self.game.getXY(self.x, self.y + direction) == None and self.game.getXY(self.x, self.y + direction * 2) == None and not self.hasMoved:
            moves.append([self.x, self.y + 2])
        return self.checkIllegalMoves(moves)

class Rook(Piece):
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(True)

class Knight(Piece):
    directions = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(False)

class Bishop(Piece):
    directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(True)

class Queen(Piece):
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(True)

class King(Piece):
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(False)