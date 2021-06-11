from typing import Iterator, Union, Literal
from game import BoardCoordinates, Game, Piece, InvalidPosition


LAST: Literal[None] = None
TestGeneratorType = Iterator[Union[tuple[str, str], tuple[None, None]]]

last_test = False
next_test = False


class InvalidTestCoords(Exception):
    """Invalid coordinates in test"""
    def __init__(self, coords: [str]):
        super().__init__(f"Invalid test received: {coords}")


class InvalidTestPiece(Exception):
    """Invalid piece selection"""
    def __init__(self, piece_coords: BoardCoordinates):
        super().__init__(f"Invalid test piece selection: {piece_coords}")


class NextTest(Exception):
    """raised when current test finishes"""
    pass


class LastTest(Exception):
    """raised when testing finishes"""
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

    def __exit__(self, exc_type, exc_val, exc_tb):  # pretty sure this doesn't work
        print(f"An exception occurred:"
              f"----------------------"
              f"Exception Type: {exc_type}"
              f"Exception Value: {exc_val}"
              f"Exception Traceback:\n{exc_tb}"
              f"\nCurrent Test: {self.test_states.keys()[-1]}"
              f"Current State: {self.test_states[self.test_states.keys()[-1]]}")
        quit(2)

    def _create_test_gen(self) -> TestGeneratorType:
        """returns an iterator for all tests"""
        for test, moves in self.tests.items():
            for move in moves:

                if move is LAST:  # if test is done
                    yield LAST, LAST

                if test != self.current_test:  # display new test name
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

            if end_state is None:  # if no test
                print("No end state")
                continue

            for line in end_state:  # print board
                print(line)

        return None, None

    def get_player_input(self, game: Game) -> Union[tuple[Piece, BoardCoordinates], tuple[None, None]]:
        """ Monkey-patched input used in main game loop"""
        try:
            test, test_coords = next(self._test_gen)

            if test is LAST and test_coords is LAST:
                next(self._test_gen)

                if self.test_states.get(self.current_test) is not None:
                    self.test_states[self.current_test] = game.board.to_ascii()  # save last state

                else:
                    self.test_states[self.current_test] = None  # prevent starting state from being saved if no test

                raise NextTest  # restart game instance + goto next test

        except StopIteration:
            raise LastTest  # break out of testing loop and display final states

        self.test_states[self.current_test] = game.board.to_ascii()  # store current board state

        try:
            piece_pos, move_pos = BoardCoordinates(-1, -1), BoardCoordinates(-1, -1)  # init to invalid positions

            # parse input
            test_coords = test_coords.split(" ")
            piece_pos.set_with_notation(test_coords[0])

            piece = game.board.get(str(piece_pos))  # get piece at pos

            if piece is None or piece.colour != game.current_player.colour:  # if invalid selection
                raise InvalidTestPiece(piece_pos)

            move_pos.set_with_notation(test_coords[1])  # move piece

            return piece, move_pos

        except InvalidPosition:  # if invalid move
            raise InvalidTestCoords(test_coords)
