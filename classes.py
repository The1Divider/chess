WHITE, BLACK, EMPTY = "WHITE", "BLACK", "EMPTY"
class Game:
    players: []
    pieces: []
    deadPieces: []
    activePlayer = None
    nonActivePlayer = None
    def __init__(self):
        self.pieces = [Rook(0, 0, BLACK, self), Knight(1, 0, BLACK, self), Bishop(2, 0, BLACK, self), Queen(3, 0, BLACK, self), King(4, 0, BLACK, self), Bishop(5, 0, BLACK, self), Knight(6, 0, BLACK, self), Rook(7, 0, BLACK, self),
                       Pawn(0, 1, BLACK, self), Pawn(1, 1, BLACK, self), Pawn(2, 1, BLACK, self), Pawn(3, 1, BLACK, self), Pawn(4, 1, BLACK, self), Pawn(5, 1, BLACK, self), Pawn(6, 1, BLACK, self), Pawn(7, 1, BLACK, self),
                       Pawn(0, 6, WHITE, self), Pawn(1, 6, WHITE, self), Pawn(2, 6, WHITE, self), Pawn(3, 6, WHITE, self), Pawn(4, 6, WHITE, self), Pawn(5, 6, WHITE, self), Pawn(6, 6, WHITE, self), Pawn(7, 6, WHITE, self),
                       Rook(0, 7, WHITE, self), Knight(1, 7, WHITE, self), Bishop(2, 7, WHITE, self), Queen(3, 7, WHITE, self), King(4, 7, WHITE, self), Bishop(5, 7, WHITE, self), Knight(6, 7, WHITE, self), Rook(7, 7, WHITE, self)]
        self.players = [Player(input("Who is playing white? "), WHITE, self), Player(input("Who is playing black? "), BLACK, self)]
        self.deadPieces = []
        self.activePlayer = self.players[0]
        self.nonActivePlayer = self.players[1]

    def cycleTurn(self):
        self.activePlayer.hasMoved = False
        self.nonActivePlayer = self.activePlayer
        self.activePlayer = self.players[0] if self.activePlayer.colour == BLACK else self.players[1]

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
    
    def getAsciiBoard(self):
        board = ["    a    b    c    d    e    f    g    h", "  " + "-" * 41]
        for y in range(8):
            row = f"{8 - y} |"
            for x in range(8):
                piece = self.getXY(x, y)
                row += f" {piece.getToken()} |" if piece != None and not piece.captured else "    |"
                # 2 + 5 * (x + 1)
                #3 | bN |    |
            board.append(row)
            board.append("  " + "-" * 41)
        return board
    
    def notationToXY(self, notation):
        notation = notation.lower()
        return [ord(notation[0]) - 97, 8 - int(notation[1])]

    def XYToNotation(self, x, y):
        return chr(97 + x) + (str)(8 - y)

class Player:
    name: str
    colour: str
    game: Game
    hasMoved: bool
    pieces: []
    def __init__(self, name, colour, game):
        self.name, self.colour, self.game, self.hasMoved = name, colour, game, False
        self.pieces = [piece for piece in self.game.pieces if piece.colour == self.colour]

    def doMove(self, piece, x, y):
        capture = self.game.getXY(x, y)      # piece/place to be captured
        piece.x, piece.y = x, y         # update piece's xy values
        self.hasMoved = True
        # if the move prompted a piece capture
        if capture != None:
            capture.x, capture.y = -1, -1   # set the xy values to off-board ones
            capture.captured = True
            self.game.nonActivePlayer.pieces.remove(capture)
            self.game.deadPieces.append(capture)
class Piece:
    x: int
    y: int
    colour: str
    hasMoved: bool
    captured: bool
    directions: []
    token: str
    game: Game
    def __init__(self, x, y, colour, game):
        self.x, self.y, self.colour, self.game = x, y, colour, game
        self.hasMoved, self.captured = False, False
    
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

    def getToken(self):
        return self.colour[0].lower() + self.token

    def toString(self):
        return f"{self.colour} {type(self)} on ({self.x}, {self.y})."

    def getPossibleBoard(self):
        board = self.game.getAsciiBoard()
        for x, y in self.getAvailableMoves():
            board[2 + y * 2] = board[2 + y * 2][:1 + 5 * (x + 1)] + "*" + board[2 + 2 * y][2 + 5 * (x + 1):]
        return board
class Pawn(Piece):
    token = "P"
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
            moves.append([self.x, self.y + direction * 2])
        return self.checkIllegalMoves(moves)
class Rook(Piece):
    token = "R"
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(True)
class Knight(Piece):
    token = "N"
    directions = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(False)
class Bishop(Piece):
    token = "B"
    directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(True)
class Queen(Piece):
    token = "Q"
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(True)
class King(Piece):
    token = "K"
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    def getAvailableMoves(self):
        return super().getAvailableMoves(False)