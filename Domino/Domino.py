import random
from enum import Enum


class Player(Enum):
    PERSON = "player"
    COMPUTER = "computer"


class Position(Enum):
    BEGIN = 0
    END = 1


class IllegalMove(Exception):
    pass


class Domino:
    def __init__(self, first, second):
        self.__vect = [first, second]

    def __contains__(self, value):
        return value in self.__vect

    def __eq__(self, other):
        return ((other.first == self.first and other.second == self.second)
                or (other.first == self.second and other.second == self.first))

    def __str__(self):
        return f"[{self.first}, {self.second}]"

    @property
    def first(self):
        return self.__vect[0]

    @first.setter
    def first(self, value):
        self.__vect[0] = value

    @property
    def second(self):
        return self.__vect[1]

    @second.setter
    def second(self, value):
        self.__vect[1] = value

    def flip(self):
        first, second = self.__vect
        self.first, self.second = second, first

    def count(self, value):
        return self.__vect.count(value)


class DominoHand:

    def __init__(self):
        self.__hand = []

    @property
    def hand(self):
        return self.__hand

    def __contains__(self, domino):
        return domino in self.__hand

    def __str__(self):
        return ("{}" * len(self.__hand)).format(*self.hand)

    def __getitem__(self, index):
        return self.__hand[index]

    def __len__(self):
        return len(self.__hand)

    def __insert(self, index, domino):
        self.__hand.insert(index, domino)

    def insert_begin(self, domino):
        self.__insert(0, domino)

    def insert_end(self, domino):
        self.__insert(len(self.__hand), domino)

    def remove(self, domino):
        self.__hand.remove(domino)

    def shuffle(self):
        random.shuffle(self.__hand)

    def pop(self, index=-1):
        value = self.__hand[index]
        del self.__hand[index]
        return value


class Snake(DominoHand):
    def __init__(self):
        super().__init__()

    @property
    def first_domino(self) -> Domino:
        return self.hand[0]

    @property
    def last_domino(self) -> Domino:
        return self.hand[-1]

    def legal_value(self):
        return self.first_domino.first, self.last_domino.second

    def insert(self, domino, position: Position):
        """
            Insert the given domino to the position, flip the domino if necessary.
            Raise IllegalMove if we cannot insert the domino.
        :param domino: The domino the player wants to insert.
        :param position: The position the player wants to insert.
        """
        if not isinstance(position, Position):
            raise ValueError

        if position == Position.BEGIN:
            # Test if the domino is on the correct direction
            if self.first_domino.first == domino.second:
                self.insert_begin(domino)
            # The domino is inverted
            elif self.first_domino.first == domino.first:
                domino.flip()
                self.insert_begin(domino)
            # If none is correct, we do not have a correct domino
            else:
                raise IllegalMove
        elif position == Position.END:
            # Test if the domino is on the correct direction
            if self.last_domino.second == domino.first:
                self.insert_end(domino)
            # The domino is inverted
            elif self.last_domino.second == domino.second:
                domino.flip()
                self.insert_end(domino)
            else:
                raise IllegalMove

    def count(self, value):
        count = 0
        for domino in self.hand:
            count += domino.count(value)
        return count

    def end_game(self):
        if self.first_domino.first == self.last_domino.second:
            value = self.first_domino.first
            if self.count(value) == 8:
                return True
        return False

    def __str__(self):
        if len(self.hand) > 6:
            return ("{}" * 3).format(*self.hand[:3]) + "..." + ("{}" * 3).format(*self.hand[-3:])
        else:
            return super().__str__()


class DominoGame:

    def __init__(self):
        self.stock_piece = DominoHand()
        self.computer_hand = DominoHand()
        self.player_hand = DominoHand()
        self.snake = Snake()
        self.status = None
        self.start_game()

    def __initialize(self):
        """
            Resplenish stock_piece with every domino
        """
        for i in range(7):
            for j in range(7):
                if Domino(i, j) not in self.stock_piece:
                    self.stock_piece.insert_end(Domino(i, j))
        self.stock_piece.shuffle()

    def __distribute(self):
        """
            Distribute seven dominoes to player and computer
        """
        for i in range(7):
            self.player_hand.insert_end(self.stock_piece.pop())
            self.computer_hand.insert_end(self.stock_piece.pop())

    def __first_piece(self):
        """
            Decide the first piece, ie the greatest double, with which player have it
        :return: computer or player or None
        """
        for i in range(6, 0, -1):
            if Domino(i, i) in self.computer_hand:
                return Player.COMPUTER, Domino(i, i)
            elif Domino(i, i) in self.player_hand:
                return Player.PERSON, Domino(i, i)
        return None, None

    def __illegal_move(self, domino, position: Position):
        """
            Decide if the given domino can be played at the given position
        :param domino: the domino the player wants to play
        :param position: the position the player wants to play
        :return: True if the given domino can be played at the given position, False otherwise
        """
        if not isinstance(position, Position):
            raise ValueError

        begin, end = self.snake.legal_value()
        if position is Position.BEGIN:
            return begin not in domino
        else:
            return end not in domino

    def __illegal_piece(self, domino):
        """
            Decide if the given domino can be played or not
        :param domino: the domino the player wants to play
        :return: True if the domino cannot be played False otherwise
        """
        return self.__illegal_move(domino, Position.BEGIN) and self.__illegal_move(domino, Position.END)

    def __end_game(self):
        if len(self.computer_hand) == 0:
            return True, Player.COMPUTER
        elif len(self.player_hand) == 0:
            return True, Player.PERSON
        else:
            if self.snake.end_game():
                return True, None
            else:
                return False, None

    def start_game(self):
        """
            install everything to begin the game
        """
        self.__initialize()
        self.__distribute()
        player, domino = self.__first_piece()

        while player is None:
            self.__initialize()
            self.__distribute()
            player, domino = self.__first_piece()

        # If a player has the greatest double, the next to play is the other
        match player:
            case Player.COMPUTER:
                self.snake.insert_end(domino)
                self.computer_hand.remove(domino)
                self.status = Player.PERSON
            case Player.PERSON:
                self.snake.insert_end(domino)
                self.player_hand.remove(domino)
                self.status = Player.COMPUTER

    def playing_field(self):
        """
            Give the interface of the game
        """
        print("=" * 70)
        print(f"Stock size: {len(self.stock_piece)}")
        print(f"Computer piece: {len(self.computer_hand)}")
        print()
        print(str(self.snake))
        print()
        print("Your pieces:")
        for index, piece in enumerate(self.player_hand.hand, start=1):
            print(f"{index}:{piece}")
            # if self.__illegal_piece(piece):
            #     print(f"{index}:{piece}")
            # else:
            #     print(f"{index}:{piece} <-")
        print()
        if self.status is Player.PERSON:
            print("Status: It's your turn to make a move. Enter your command")
        elif self.status is Player.COMPUTER:
            print("Status: Computer is about to make a move. Press Enter to continue...")

    def pick(self, player: Player = Player.PERSON):
        """
            The given player decide to take a piece from the stock piece, raise IllegalMove if the stock is empty
        :param player: The player who take the piece
        """
        # If it is empty, we do nothing and the player skip turns
        if len(self.stock_piece) != 0:
            match player:
                case Player.PERSON:
                    self.player_hand.insert_end(self.stock_piece.pop())
                case Player.COMPUTER:
                    self.computer_hand.insert_end(self.stock_piece.pop())


    def __read_input(self):
        """
            Read and validate the user input
        :return: the position, he wants to play and the index of the domino
        """
        good_input = False
        while not good_input:
            try:
                index = int(input())
                if not -len(self.player_hand) <= index <= len(self.player_hand):
                    raise ValueError
            except ValueError:
                print("Invalid input. Please try again.")
            else:
                good_input = True
        # We do not need to correct for choice 0 as it means to pick
        if index == 0:
            return None, index
        elif index > 0:
            return Position.END, index
        else:
            index *= -1
            return Position.BEGIN, index

    def player_turn(self):
        """
            Define the action for the player turn
        """
        position, index = self.__read_input()

        if index == 0:
            self.pick()
        else:
            # We want to play, we substract to have the correct index
            index -= 1
            domino = self.player_hand[index]
            if self.__illegal_move(domino, position):
                raise IllegalMove
            self.snake.insert(domino, position)
            self.player_hand.remove(domino)

    def computer_turn(self):
        """
            Define the action for the computer turn
        """
        counter = { i: 0 for i in range(7)}
        for k in counter.keys():
            for domino in self.computer_hand.hand + self.snake.hand:
                counter[k] += domino.count(k)

        scored_hand = list(sorted(self.computer_hand.hand, key=lambda d: counter[d.first] + counter[d.second],reverse=True))

        has_played = False
        for domino in scored_hand:
            if not self.__illegal_piece(domino):
                if not self.__illegal_move(domino, Position.BEGIN):
                    self.snake.insert(domino, Position.BEGIN)
                    self.computer_hand.remove(domino)
                    has_played = True
                    break
                elif not self.__illegal_move(domino, Position.END):
                    self.snake.insert(domino, Position.END)
                    self.computer_hand.remove(domino)
                    has_played = True
                    break
        if not has_played:
            self.pick(Player.COMPUTER)

    def play(self):
        """
            The method for all the process of the game
        """
        endgame = False
        winner = None
        good_move = True
        while not endgame:
            if good_move:
                self.playing_field()
            match self.status:
                case Player.PERSON:
                    try:
                        self.player_turn()
                    except IllegalMove:
                        good_move = False
                        print("Illegal move. Please try again.")
                    else:
                        good_move = True
                        self.status = Player.COMPUTER
                case Player.COMPUTER:
                    try:
                        self.computer_turn()
                    except IllegalMove:
                        good_move = False
                    else:
                        good_move = True
                        self.status = Player.PERSON
                        input()

            endgame, winner = self.__end_game()

        if endgame:
            self.playing_field()
            if winner is None:
                print("Status: The game is over. It's a draw")
            elif winner is Player.PERSON:
                print("Status: The game is over. You won")
            elif winner is Player.COMPUTER:
                print("Status: The game is over. The computer won")

    def __repr__(self):
        return (f"Stock pieces: {self.stock_piece}\n"
                f"Computer pieces: {self.computer_hand}\n"
                f"Player pieces: {self.player_hand}\n"
                f"Domino snake: {self.snake}\n"
                f"Status: {self.status.value}")


if __name__ == "__main__":
    game = DominoGame()
    game.play()
