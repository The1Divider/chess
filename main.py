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
    print("\nHelp for h4ck3rch3ss:\n - help: prints this help message\n - possible <piece>: view the possible moves for <piece>\n - board: prints out the current board\n - move <piece>: take your turn and move <piece>. once you run move, you must move the piece you pick\n - forfeit: admit defeat and immediately lose the game\n")

def board():
    print('\n'.join(game.getAsciiBoard()))

def possible(choice):
    x, y = game.notationToXY(choice)
    piece = game.getXY(x, y)
    if piece == None or piece.colour != player.colour:
        print("Invalid choice.")
    moves = [game.XYToNotation(x, y) for [x, y] in piece.getAvailableMoves()]
    if moves != []:
        print('\n'.join(piece.getPossibleBoard()))
    else:
        print("No possible moves for that piece, exiting.")

def move(choice):
    x, y = game.notationToXY(choice)
    piece = game.getXY(x, y)
    if piece == None or piece.colour != player.colour:
        print("Invalid choice.")
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
        command = input(">>> ").lower()
        while command.split()[0] not in commands.keys():
            print("Invalid command. Type 'help' for help.")
            command = input(">>> ").lower()
        if len(command.split()) == 1 and (command == "move" or command == "possible"):
            print(f"You must provide a parameter for {command}.")
        elif len(command.split()) == 1:
            commands[command]()
        else:
            commands[command.split()[0]](command.split()[1])
    game.cycleTurn()