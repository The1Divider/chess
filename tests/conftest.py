import pytest

tests = {
            "White Castling": ["g2 g3", "a7 a6", "g1 f3", "b7 b6", "f1 h3", "c7 c6", "e1 g1", None],
            "Black Castling": ["a2 a3", "g7 g6", "b2 b3", "f8 h6", "c2 c3", "g8 f6", "d2 d3", "e8 g8", None],
            "White En Passant": ["a2 a4", "a7 a6", "a4 a5", "b7 b5", "a5 b6", None],
            "Black En Passant": ["a2 a3", "a7 a5", "c2 c3", "a5 a4", "b2 b4", "a4 b3", None],
            "Checkmate": ["f2 f3", "e7 e5", "g2 g4", "d8 h4", None],
            "Draw - Threefold repetition": ["e2 e3", "e7 e6", "e1 e2", "e8 e7", "e2 e1", "e7 e8", "e1 e2", "e8 e7",
                                            "e2 e1", "e7 e8", "e1 e2", "e8 e7", "e2 e1", "e7 e8"],
            "Draw - No More Moves": [None],
            "Draw - Lack of Pieces": [None]
        }

#-> tuple[Player, Player]
def start() :
    return game.Player("WHITE", game.WHITE), Player("BLACK", game.BLACK)


def get_player_input(game):
    """ Monkey-patched input used in main game loop"""


@pytest.fixture(scope="function")
def get_game():
    _chess = main.Chess
    _chess.start = start
    _chess.get_player_input = get_player_input

    return Chess()
