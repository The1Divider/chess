from typing import Iterator, Union, Literal
from game import BoardCoordinates, Game, Piece, InvalidPosition


LAST: Literal[None] = None
last_test = False
next_test = False


TestGeneratorType = Iterator[Union[tuple[str, str], tuple[None, None]]]


class InvalidTestCoords(Exception):
    def __init__(self, coords: [str]):
        super().__init__(f"Invalid test received: {coords}")


class InvalidTestPiece(Exception):
    def __init__(self, piece_coords: BoardCoordinates):
        super().__init__(f"Invalid test piece selection: {piece_coords}")


class TestsFinished(Exception):
    def __init__(self):
        super().__init__()


class NextTest(Exception):
    pass


class LastTest(Exception):
    pass


class Test:
    def __init__(self):
        self.current_test = None
        self.tests_finished = False

        self.test_states = {}

        self.tests = {
            "White Castling": ["g2 g3", "a7 a6", "g1 f3", "b7 b6", "f1 h3", "c7 c6", "e1 g1", None],
            "Black Castling": ["a2 a3", "g7 g6", "b2 b3", "f8 h6", "c2 c3", "g8 f6", "d2 d3", "e8 g8", None],
            "White En Passant": ["a2 a4", "a7 a6", "a4 a5", "b7 b5", "a5 b6", None],
            "Black En Passant": ["a2 a3", "a7 a5", "c2 c3", "a5 a4", "b2 b4", "a4 b3", None],
            "Checkmate": ["f2 f3", "e7 e5", "g2 g4", "d8 h4", None],
            "Draw - No More Moves": [None],
            "Draw - Lack of Pieces": [None]
        }

        self._test_gen = self._create_test_gen()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"An exception occurred:"
              f"----------------------"
              f"Exception Type: {exc_type}"
              f"Exception Value: {exc_val}"
              f"Exception Traceback:\n{exc_tb}"
              f"\nCurrent Test: {self.test_states.keys()[-1]}"
              f"Current State: {self.test_states[self.test_states.keys()[-1]]}")
        quit(2)

    def _create_test_gen(self) -> TestGeneratorType:
        for test, moves in self.tests.items():
            for move in moves:

                if move is LAST:
                    yield LAST, LAST

                if test != self.current_test:
                    print(f"Test: {test}")
                    self.current_test = test

                yield test, move

    def finished_tests(self) -> tuple[None, None]:
        print(f"\n----------------------------------"
              f"All tests passed!"
              f"----------------------------------\n\n"
              f"States:")

        for test, end_state in self.test_states.items():
            print(f"\nTest: {test}")

            if end_state is None:
                print("No end state")

            for line in end_state:
                print(line)

        return None, None

    def get_player_input(self, game: Game) -> Union[tuple[Piece, BoardCoordinates], tuple[None, None]]:
        try:
            test, test_coords = next(self._test_gen)

            if test is LAST and test_coords is LAST:
                next(self._test_gen)
                self.test_states[self.current_test] = game.board.to_ascii()
                raise NextTest
            print(test, test_coords)
        except StopIteration:
            raise LastTest

        self.test_states[self.current_test] = game.board.to_ascii()

        try:
            piece_pos, move_pos = BoardCoordinates(-1, -1), BoardCoordinates(-1, -1)
            test_coords = test_coords.split(" ")
            piece_pos.set_with_notation(test_coords[0])

            piece = game.board.get(str(piece_pos))

            if piece is None or piece.colour != game.current_player.colour:
                raise InvalidTestPiece(piece_pos)

            move_pos.set_with_notation(test_coords[1])

            return piece, move_pos

        except InvalidPosition:
            raise InvalidTestCoords(test_coords)
