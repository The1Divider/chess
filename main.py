''' Game board with x, y for reference
0, 0	1, 0	2, 0	3, 0	4, 0	5, 0	6, 0	7, 0
0, 1	1, 1	2, 1	3, 1	4, 1	5, 1	6, 1	7, 1
0, 2	1, 2	2, 2	3, 2	4, 2	5, 2	6, 2	7, 2
0, 3	1, 3	2, 3	3, 3	4, 3	5, 3	6, 3	7, 3
0, 4	1, 4	2, 4	3, 4	4, 4	5, 4	6, 4	7, 4
0, 5	1, 5	2, 5	3, 5	4, 5	5, 5	6, 5	7, 5
0, 6	1, 6	2, 6	3, 6	4, 6	5, 6	6, 6	7, 6
0, 7	1, 7	2, 7	3, 7	4, 7	5, 7	6, 7	7, 7
'''
# main gameplay logic file
from classes import *
game = Game()

def help():
    print("\nHelp for h4ck3rch3ss:\n - help: prints this help message\n - board: prints out the current board\n - move: take your turn and move a piece\n - possible: lists possible moves\n - forfeit: admit defeat and immediately lose the game\n")

def board():
    print("this function has yet to be implemented due to a lazy developer")

def move():
    print("this function has yet to be implemented due to a lazy developer")

def possible():
    print("this function has yet to be implemented due to a lazy developer")

def forfeit():
    print("this function has yet to be implemented due to a lazy developer")

commands = {"help": help,
            "board": board,
            "move": move,
            "possible": possible}

print(game.getAsciiBoard())