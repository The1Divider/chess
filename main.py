import sys
from typing import Generator, Iterator

from game import *


TestGeneratorType = Iterator[Union[tuple[str, str], tuple[None, None]]]

DEBUG = True
last_test = False
next_test = False


class InvalidTestCoords(Exception):
    def __init__(self, coords: [str]):
        super().__init__(f"Invalid test received: {coords}")


class InvalidTestPiece(Exception):
    def __init__(self, piece_coords: BoardCoordinates):
        super().__init__(f"Invalid test piece selection: {piece_coords}")


class TestsFinished(Exception):
    def __init__(self):
        super().__init__()


class Test:
    LAST: Literal[None] = None

    def __init__(self):
        self.current_test = None
        self.tests_finished = False

        self.test_states = {}

        self.tests = {"Castling": ["g2 g3", "a7 a6", "g1 f3", "b7 b6", "f1 g2", "c7 c6", "e1 g1", None],
                      "En Passant": ["a2 a4", "a7 a6", "a4 a5", "b7 b5", "a5 b6", None],
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

                if move is self.LAST:
                    raise NextTest

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

            for line in end_state:
                print(line)

        return None, None

    def get_player_input(self, game: Game) -> Union[tuple[Piece, BoardCoordinates], tuple[None, None]]:
        try:
            test, test_coords = next(self._test_gen)
        except StopIteration:
            raise LastTest

        self.test_states[test] = game.board.to_ascii()

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


class Chess:
    def __init__(self):
        self.player_1, self.player_2 = self.start()
        self.game = Game(self.player_1, self.player_2)

    def start_game_loop(self):
        self._game_loop()

    @staticmethod
    def start() -> tuple[Player, Player]:
        if DEBUG:
            return Player("white", WHITE), Player("black", BLACK)

        player_1_name = input("Player 1: ")
        player_2_name = input("Player 2: ")

        return Player(player_1_name, WHITE), Player(player_2_name, BLACK)

    def get_player_input(self, game: Optional[Game] = None):
        player_input = input(">").split(" ")

        if len(player_input) > 2:
            print(f"Invalid input: {player_input}")
            return None

        piece_input = player_input[0]
        piece = self.game.board.get(piece_input)

        if piece is None or piece.colour != self.game.current_player.colour:
            print(f"Invalid piece selection: {piece_input}")
            return None

        if len(player_input) == 1:
            move_pos_input = input("Enter move position: ")
        else:
            move_pos_input = player_input[1]

        try:
            temp_move_pos = BoardCoordinates(-1, -1)
            temp_move_pos.set_with_notation(move_pos_input)
            move_pos = temp_move_pos

        except InvalidPosition:
            print(f"Invalid move position input: {move_pos_input}")
            return None

        return piece, move_pos

    def _game_loop(self):
        move_status = None
        while move_status not in (MoveStatus.KING_IN_CHECKMATE, MoveStatus.DRAW):

            for row in self.game.board.to_ascii():
                print(row)

            piece, move_pos = self.get_player_input() if not DEBUG else self.get_player_input(self.game)

            if piece is None or move_pos is None:
                continue

            move_status = self.game.make_move(piece, move_pos)

            if move_status == MoveStatus.INVALID_MOVE:
                print(f"Invalid move position: {move_pos.get_notation()}")

            elif move_status == MoveStatus.PUTS_KING_IN_CHECK:
                print(f"Invalid move, puts king in check: {move_pos.get_notation()}")

            elif move_status == MoveStatus.VALID_MOVE:
                self.game.next_turn()

            elif move_status == MoveStatus.KING_IN_CHECKMATE:
                print(f"\nCheckmate, "
                      f"{self.player_1 if self.game.current_player == self.player_2.colour else self.player_2}"
                      f" wins!")
            elif move_status == MoveStatus.DRAW:
                print(f"Game over, draw")

            else:
                raise Exception(f"Move status: '{move_status}' received")


class NextTest(Exception):
    pass

class LastTest(Exception):
    pass


if DEBUG:
    tests = Test()
    try:
        while True:
            current_game = Chess()
            current_game.get_player_input = tests.get_player_input
            try:
                current_game.start_game_loop()
            except NextTest:
                pass
    except LastTest:
        tests.finished_tests()
else:
    current_game = Chess()
    current_game.start_game_loop()



