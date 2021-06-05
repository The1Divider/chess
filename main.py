import sys

from game import *

DEBUG = True
current_test = None
tests_finished = False


def debug():
    tests = {"castling": [["g2 g3"], ["a7 a6"], ["g1 f3"], ["b7 b6"], ["f1 g2"], ["c7 c6"], ["e1 g1"]],
             "test": [["a2 a4"]]}
    test_number = 0
    for test, moves in tests.items():
        test_number += 1
        for move in moves:
            yield test_number
            yield test, *move


def start() -> Game:
    if DEBUG:
        return Game(Player("white", WHITE), Player("black", BLACK))

    player_1_name = input("Player 1: ")
    player_1 = Player(player_1_name, WHITE)
    player_2_name = input("Player 2: ")
    player_2 = Player(player_2_name, BLACK)

    return Game(player_1, player_2)


def get_input(test_gen):
    if DEBUG:
        # use tests

        global current_test

        try:
            test, player_input = next(test_gen)

            if current_test != test:

                if current_test is not None:
                    print("\n----------------------------------")
                    print(f"{current_test} test successful!")
                    print("----------------------------------\n")

                print("\n----------------------------------")
                print(f"Testing {test}...")
                print("----------------------------------\n")
                print(player_input)

                current_test = test

            return player_input.split(" ")

        except StopIteration:
            quit(69)
    else:
        # use + parse player input
        player_input = input(">").split(" ")

        if len(player_input) > 2:
            print(f"Invalid input: {player_input}")

        return player_input


def main(test_gen):

    game = start()

    test_number = 1
    move_status = None
    new_test = False
    move_pos = None
    while move_status != MoveStatus.KING_IN_CHECKMATE:
        global tests_finished

        game.board.display_ascii_board()
        # game.board.to_fen(game)

        piece, move_position = None, None
        while piece is None or move_position is None:
            if DEBUG:
                try:
                    new_test_number = next(test_gen)
                    if new_test_number != test_number:
                        new_test = True
                        break
                except StopIteration:
                    print("\n----------------------------------")
                    print(f"All tests passed!")
                    print("----------------------------------\n")
                    tests_finished = True
                    break

            player_input = get_input(test_gen)

            try:
                piece = game.board.get(player_input[0])

                if piece is None or piece.colour != game.current_player.colour:
                    raise KeyError

            except KeyError:
                print(f"Invalid piece selection: {player_input[0]}")
                if DEBUG:
                    break

                continue

            try:

                if len(player_input) == 2:
                    move_position = player_input[1]

                else:
                    move_position = input("Enter move position: ")

                move_pos = BoardCoordinates(-1, -1)
                move_pos.set_with_notation(move_position)

            except InvalidPosition:

                print(f"Invalid move position input: {move_position}")

                if DEBUG:
                    break

                move_position = None
                continue

        if DEBUG and new_test or tests_finished:
            break

        move_status = game.make_move(piece, move_pos)

        if move_status == MoveStatus.INVALID_MOVE:
            print(f"Invalid move position: {move_position}")
            if DEBUG:
                break

        elif move_status == MoveStatus.PUTS_KING_IN_CHECK:
            print(f"Invalid move, puts king in check: {move_position}")
            if DEBUG:
                break

        elif move_status == MoveStatus.VALID_MOVE:
            game.next_turn()

        else:
            raise Exception(f"Move status: '{move_status}' received")


if __name__ == "__main__":
    test_gen = debug()
    while not tests_finished:
        main(test_gen)
    print(":)")


