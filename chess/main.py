from random import randint

from game import *


class Chess:
    def __init__(self):
        self.player_1, self.player_2 = self.start()
        self.game = Game(self.player_1, self.player_2)

    def start_game_loop(self):
        self._game_loop()

    def start(self) -> tuple[Player, Player]:
        player_1_name = input("Player 1: ")
        player_2_name = input("Player 2: ")

        player_1_colour = WHITE if randint(0, 1) == 0 else BLACK
        player_2_colour = BLACK if player_1_colour == WHITE else BLACK

        return Player(player_1_name, player_1_colour), Player(player_2_name, player_2_colour)

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

            piece, move_pos = self.get_player_input(self.game)

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


if __name__ == "__main__":
    current_game = Chess()
    current_game.start_game_loop()
