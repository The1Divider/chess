''' Game board with x, y for reference
   a        b       c       d       e       f       g       h
8  0, 0	    1, 0	2, 0	3, 0	4, 0	5, 0	6, 0	7, 0
7  0, 1	    1, 1	2, 1	3, 1	4, 1	5, 1	6, 1	7, 1
6  0, 2	    1, 2	2, 2	3, 2	4, 2	5, 2	6, 2	7, 2
5  0, 3	    1, 3	2, 3	3, 3	4, 3	5, 3	6, 3	7, 3
4  0, 4	    1, 4	2, 4	3, 4	4, 4	5, 4	6, 4	7, 4
3  0, 5	    1, 5	2, 5	3, 5	4, 5	5, 5	6, 5	7, 5
2  0, 6	    1, 6	2, 6	3, 6	4, 6	5, 6	6, 6	7, 6
1  0, 7	    1, 7	2, 7	3, 7	4, 7	5, 7	6, 7	7, 7
'''
# main gameplay logic file
from classes import *
game = Game()

def help():
    print("\nHelp for h4ck3rch3ss:\n - help: prints this help message\n - board: prints out the current board\n - move: take your turn and move a piece\n - forfeit: admit defeat and immediately lose the game\n")

def board():
    print('\n'.join(game.getAsciiBoard()))

def possible():
    x, y = game.notationToXY(input("Select the piece you want to view: "))
    piece = game.getXY(x, y)
    while piece == None or piece.colour != player.colour:
        x, y = game.notationToXY(input("Invalid choice, select another piece: "))
        piece = game.getXY(x, y)
    print('\n'.join(piece.getPossibleBoard()))

def move():
    x, y = game.notationToXY(input("Select the piece you want to move: "))
    piece = game.getXY(x, y)
    while piece == None or piece.colour != player.colour:
        x, y = game.notationToXY(input("Invalid choice, select another piece: "))
        piece = game.getXY(x, y)
    moves = [game.XYToNotation(x, y) for [x, y] in piece.getAvailableMoves()]
    if moves != []:
        print('\n'.join(piece.getPossibleBoard()))
        move = input("Input your move: ")
        while move not in moves:
            move = input("Invalid choice, try again: ")
        x, y = game.notationToXY(move)
        player.doMove(piece, x, y)
    else:
        print("No possible moves for that piece, exiting.")

def forfeit():
    print("this function has yet to be implemented due to a lazy developer")

commands = {"help": help,
            "board": board,
            "move": move,
            "possible":possible}

over = False
while not over:
    player = game.activePlayer
    print(f"It is {player.name}'s turn. {player.name} is playing {player.colour}.")
    while not player.hasMoved:
        command = input(">>> ")
        while command not in commands.keys():
            print("Invalid command. Type 'help' for help.")
            command = input(">>> ")
        commands[command]()
    game.cycleTurn()