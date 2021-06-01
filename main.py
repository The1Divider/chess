from game import *


def start() -> Game:
    player_1_name = input("Player 1: ")
    player_1 = Player(player_1_name, WHITE)
    player_2_name = input("Player 2: ")
    player_2 = Player(player_2_name, BLACK)

    return Game(player_1, player_2)


def main():
    game = start()

    move_status = None
    while move_status != MoveStatus.KING_IN_CHECKMATE:
        game.board.display_ascii_board()
        # game.board.to_fen(game)
        print(game.en_passant_target)
        print(game.current_player.colour)

        piece, move_position = None, None
        while piece is None or move_position is None:
            player_input = input(">").split(" ")

            if len(player_input) > 2:
                print(f"Invalid input: {player_input}")

            try:
                piece = game.board.get(player_input[0])
                if piece is None:
                    raise KeyError
            except KeyError:
                print(f"Invalid piece selection: {player_input[0]}")
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
                move_position = None
                continue

        move_status = game.make_move(piece, move_pos)

        if move_status == MoveStatus.INVALID_MOVE:
            print(f"Invalid move position: {move_position}")
        elif move_status == MoveStatus.PUTS_KING_IN_CHECK:
            print(f"Invalid move, puts king in check: {move_position}")
        elif move_status == MoveStatus.VALID_MOVE:
            game.next_turn()


if __name__ == "__main__":
    main()


