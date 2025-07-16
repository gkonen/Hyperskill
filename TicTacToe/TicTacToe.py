# write your code here
import itertools

from enum import Enum


class Player(Enum):
    Player1= "X"
    Player2= "O"

class TicTacToe:

    def __init__(self):
        self.board = [['_' for _ in range(3)] for _ in range(3)]

    @property
    def flatten(self):
        return list(itertools.chain(*self.board))

    def __check_row(self, player : Player ):
        test = False
        for i in range(3):
            if self.board[0][i] == player.value:
                test = self.board[0][i] == self.board[1][i] == self.board[2][i]
                if test:
                    break
        return test

    def __check_column(self, player : Player ):
        test = False
        for i in range(3):
            if self.board[i][0] == player.value:
                test = self.board[i][0] == self.board[i][1] == self.board[i][2]
                if test:
                    break
        return test

    def __check_diagonal(self, player : Player ):
        test = False
        if self.board[0][0] == player.value:
            test = self.board[0][0] == self.board[1][1] == self.board[2][2]
            if test:
                return test
        if self.board[0][2] == player.value:
            test = self.board[0][2] == self.board[1][1] == self.board[2][0]
            if test:
                return test
        return test

    def has_won(self, player : Player):
        return self.__check_row(player) or self.__check_column(player) or self.__check_diagonal(player)

    def empty_cases(self):
        return "_" in self.flatten

    def status(self):
        # First, we check the impossible situation :
        if self.has_won(Player.Player1) and self.has_won(Player.Player2):
            print("Impossible")
        else:
            count_x = self.flatten.count(Player.Player1.value)
            count_o = self.flatten.count(Player.Player2.value)
            if abs(count_x - count_o) > 1:
                print("Impossible")
            else:
                # check is there is a winner
                if self.has_won(Player.Player1) :
                    print(f"{Player.Player1.value} wins")
                elif self.has_won(Player.Player2):
                    print(f"{Player.Player2.value} wins")
                else :
                    # the game is not impossible, without winner
                    # check is finished
                    if "_" in self.flatten:
                        print("Game not finished")
                    else:
                        # the game have no winner and no blanck
                        print("Draw")

    def play_move(self, row, column, player):
        if self.board[row][column] == "_":
            self.board[row][column] = player.value
        else:
            raise IndexError

    def board_game(self):
        print("---------")
        for row in self.board:
            print("|", end=" ")
            print(" ".join(map(lambda val: " " if val == "_" else val, row)), end=" ")
            print("|")
        print("---------")
        #self.status()

    @classmethod
    def from_string(cls, str_value, player: Player):
        grid = [list(str_value[:3]), list(str_value[3:6]), list(str_value[6:])]
        obj = cls(player)
        obj.board = grid
        return obj

if __name__ == "__main__":

    player = Player.Player1
    game = TicTacToe()
    game.board_game()

    game_end = False
    while not game_end:
        good_input = False
        while not good_input:
            x, y = input().split()
            if x.isdigit() and y.isdigit():
                x = int(x)
                y = int(y)
                if 1 <= x <= 3 and 1 <= y <= 3:
                    try:
                        game.play_move(x-1, y-1, player)
                    except IndexError:
                        print("This cell is occupied! Choose another one!")
                    else:
                        good_input = True
                        if game.has_won(player):
                            game_end = True
                        elif game.empty_cases():
                            if player == Player.Player1:
                                player = Player.Player2
                            elif player == Player.Player2:
                                player = Player.Player1
                        else:
                            game_end = True
                else:
                    print("Coordinates should be from 1 to 3!")
            else:
                print("You should enter numbers!")
            game.board_game()

    if game.has_won(player):
        print(f"{player.value} wins")
    else:
        print("Draw")
