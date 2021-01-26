# main gameplay logic file
from classes import *
game = Game()
for piece in game.pieces:
    print(piece.toString())