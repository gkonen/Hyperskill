import random
from enum import Enum


class Player(Enum):
    PERSON = "player"
    COMPUTER = "computer"


class Snake:
    def __init__(self):
        self.domino_snake = []

    @property
    def domino(self):
        return self.domino_snake

    @property
    def first_domino(self):
        return self.domino_snake[0]

    @property
    def last_domino(self):
        return self.domino_snake[-1]

    def count(self, value):
        count = 0
        for domino in self.domino_snake:
            count += domino.count(value)
        return count

    def end_game(self):
        if self.first_domino[0] == self.last_domino[1]:
            value = self.first_domino[0]
            if self.count(value) == 8:
                return True
        return False

    def append(self, domino):
        self.domino_snake.append(domino)

    def insert(self, domino):
        self.domino_snake.insert(0, domino)

    def __str__(self):
        if len(self.domino_snake) > 6:
            return ("{}" * 3).format(*self.domino_snake) + "..." + ("{}" * 3).format(*self.domino_snake)
        else:
            return ("{}" * len(self.domino_snake)).format(*self.domino_snake)


class Domino:

    def __init__(self):
        self.stock_piece = []
        self.computer_piece = []
        self.player_piece = []
        self.domino_snake = Snake()
        self.status = None
        self.start_game()

    def initialize(self):
        """
            Resplenish stock_piece with every domino
        """
        for i in range(7):
            for j in range(i, 7):
                if [i, j] not in self.stock_piece:
                    self.stock_piece.append([i, j])
        random.shuffle(self.stock_piece)

    def distribute(self):
        """
            Distribute seven dominoes to player and computer
        """
        for i in range(14):
            if i % 2 == 0:
                self.player_piece.append(self.stock_piece.pop())
            else:
                self.computer_piece.append(self.stock_piece.pop())

    def first_piece(self):
        """
            Decide the first piece, ie the greatest double, with which player have it
        :return: computer or player or None
        """
        for i in range(6, 0, -1):
            if [i, i] in self.computer_piece:
                return Player.COMPUTER, [i, i]
            elif [i, i] in self.player_piece:
                return Player.PERSON, [i, i]
        return None, None

    def start_game(self):
        """
            install everything to begin the game
        """
        self.initialize()
        self.distribute()
        player, domino = self.first_piece()

        while player is None:
            self.initialize()
            self.distribute()
            player, domino = self.first_piece()

        # If a player has the greatest double, the next to play is the other
        if player is Player.COMPUTER:
            self.domino_snake.append(domino)
            self.computer_piece.remove(domino)
            self.status = Player.PERSON
        elif player is Player.PERSON:
            self.domino_snake.append(domino)
            self.player_piece.remove(domino)
            self.status = Player.COMPUTER

    def playing_field(self):
        """
            Give the interface of the game
        """
        print("=" * 70)
        print(f"Stock size: {len(self.stock_piece)}")
        print(f"Computer piece: {len(self.computer_piece)}")
        print()
        print(str(self.domino_snake))
        print()
        print("Your pieces:")
        for index, piece in enumerate(self.player_piece, start=1):
            print(f"{index}:{piece}")
        print()
        if self.status is Player.PERSON:
            print("Status: It's your turn to make a move. Enter your command")
        elif self.status is Player.COMPUTER:
            print("Status: Computer is about to make a move. Press Enter to continue...")

    def player_turn(self):
        index = None
        while index is None:
            try:
                index = int(input())
                if not -len(self.player_piece) <= index <= len(self.player_piece):
                    raise ValueError
            except ValueError:
                index = None
                print("Invalid input. Please try again.")

        if index == 0:
            self.pick()
        elif index > 0:
            self.domino_snake.append(self.player_piece[index - 1])
            self.player_piece.remove(self.player_piece[index - 1])
        else:
            index *= -1
            self.domino_snake.insert(self.player_piece[index - 1])
            self.player_piece.remove(self.player_piece[index - 1])
        self.status = Player.COMPUTER

    def computer_turn(self):
        index = random.randint(-len(self.computer_piece), len(self.computer_piece))

        if index == 0:
            print("Computer pioche")
            self.pick(Player.COMPUTER)
        elif index > 0:
            print("Computer play :", self.computer_piece[index - 1])
            self.domino_snake.append(self.computer_piece[index - 1])
            self.computer_piece.remove(self.computer_piece[index - 1])
        else:
            index *= -1
            print("Computer play :", self.computer_piece[index - 1])
            self.domino_snake.insert(self.computer_piece[index - 1])
            self.computer_piece.remove(self.computer_piece[index - 1])
        input()
        self.status = Player.PERSON

    def pick(self, player: Player = Player.PERSON):
        if len(self.stock_piece) == 0:
            print("Empty stock")
        else:
            match player:
                case Player.PERSON:
                    self.player_piece.append(self.stock_piece.pop())
                case Player.COMPUTER:
                    self.computer_piece.append(self.stock_piece.pop())

    def check_win(self):
        if self.domino_snake.end_game():
            return None
        else:
            pass

    def play(self):
        while not self.domino_snake.end_game():
            self.playing_field()
            if self.status is Player.PERSON:
                self.player_turn()
            elif self.status is Player.COMPUTER:
                self.computer_turn()

    def __repr__(self):
        print("Stock pieces:", self.stock_piece)
        print("Computer pieces:", self.computer_piece)
        print("Player pieces:", self.player_piece)
        print("Domino snake:", self.domino_snake)
        print("Status:", self.status.value)


if __name__ == "__main__":
    game = Domino()
    game.play()
