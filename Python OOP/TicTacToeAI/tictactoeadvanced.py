from enum import Enum
from random import randint
from abc import ABC, abstractmethod


class CellOccupiedError(Exception):
    pass


class DimensionsError(Exception):
    pass


class GameDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    @classmethod
    def from_value(cls, value: str):
        return cls(value)


class PlayerSymbol(Enum):
    ONE = "X"
    TWO = "O"

    @classmethod
    def from_value(cls, value: str):
        return cls(value)


class CellState(Enum):
    EMPTY = "_"
    X = PlayerSymbol.ONE
    O = PlayerSymbol.TWO

    @classmethod
    def from_value(cls, value: str | PlayerSymbol):
        if value == "_":
            return cls(value)
        else:
            return cls(PlayerSymbol.from_value(value))

    def get_value(self):
        if self == CellState.EMPTY:
            return self.value
        else:
            return self.value.value

    def get_adversary(self):
        if self == CellState.X:
            return CellState.O
        elif self == CellState.O:
            return CellState.X
        return None


class Position:
    MIN = 1
    MAX = 3

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_index(self) -> tuple[int, int]:
        return self.x - 1, self.y - 1

    def is_valid(self) -> bool:
        return Position.MIN <= self.x <= Position.MAX and Position.MIN <= self.y <= Position.MAX

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x} {self.y})"


class Grid:
    winner_line = [
        [Position(1, 1), Position(1, 2), Position(1, 3)],  # 1st line
        [Position(2, 1), Position(2, 2), Position(2, 3)],  # 2nd line
        [Position(3, 1), Position(3, 2), Position(3, 3)],  # 3rd line
        [Position(1, 1), Position(2, 1), Position(3, 1)],  # 1st column
        [Position(1, 2), Position(2, 2), Position(3, 2)],  # 2nd column
        [Position(1, 3), Position(2, 3), Position(3, 3)],  # 3rd column
        [Position(1, 1), Position(2, 2), Position(3, 3)],  # 1st diagonal
        [Position(1, 3), Position(2, 2), Position(3, 1)]  # 2nd diagonal
    ]

    def __init__(self):
        self._board: list[list[CellState]] = [[CellState.EMPTY for _ in range(3)] for _ in range(3)]

    def get_cell(self, position: Position) -> CellState:
        i, j = position.get_index()
        return self._board[i][j]

    def set_cell(self, position, value: CellState):
        i, j = position.get_index()
        self._board[i][j] = value

    def linearize(self) -> list[CellState]:
        return [cell for row in self._board for cell in row]

    def is_empty(self, position: Position) -> bool:
        return self.get_cell(position) == CellState.EMPTY

    def is_win(self, state: CellState) -> bool:
        for line in Grid.winner_line:
            if all(map(lambda position: self.get_cell(position) == state, line)):
                return True
        return False

    def almost_win(self, winning_pattern: set[str]) -> list[Position] | None:
        for line in Grid.winner_line:
            line_value = ''.join(self.get_cell(position).get_value() for position in line)
            if line_value in winning_pattern:
                return line
        return None

    def __str__(self):
        line = "-" * 9
        result = line + "\n"
        for i in range(3):
            result += "| "
            for j in range(3):
                result += f"{self._board[i][j].get_value() if self._board[i][j] != CellState.EMPTY else ' '} "
            result += "|\n"
        result += line
        return result


class Player(ABC):
    _X_PATTERNS = {
        "XX_",
        "X_X",
        "_XX"
    }

    _O_PATTERNS = {
        "OO_",
        "O_O",
        "_OO"
    }

    def __init__(self, symbol: PlayerSymbol):
        self.symbol = symbol.value
        self._cell_state = CellState.from_value(symbol)

    @abstractmethod
    def play_move(self, grid: Grid):
        pass

    @property
    def cell_state(self):
        return self._cell_state

    def get_win_pattern(self, cell_state: CellState):
        if cell_state == CellState.X:
            return Player._X_PATTERNS
        elif cell_state == CellState.O:
            return Player._O_PATTERNS
        else:
            return None


class HumanPlayer(Player):
    def __init__(self, symbol: PlayerSymbol):
        super().__init__(symbol)

    def play_move(self, grid: Grid):
        while True:
            try:
                # ValueError is raised by int() if the input is not a number
                x, y = map(int, input("Enter the coordinates: ").split())
                position = Position(x, y)
                if position.is_valid():
                    if grid.is_empty(position):
                        grid.set_cell(position, self.cell_state)
                        break
                    else:
                        raise CellOccupiedError
                else:
                    raise DimensionsError
            except ValueError:
                print("You should enter numbers!")
            except CellOccupiedError:
                print("This cell is occupied! Choose another one!")
            except DimensionsError:
                print("Coordinates should be from 1 to 3!")


class ComputerPlayer(Player):

    def __init__(self, difficulty: GameDifficulty, symbol: PlayerSymbol):
        super().__init__(symbol)
        self._difficulty = difficulty

    def easy_move(self, grid):
        good_move = False
        while not good_move:
            x = randint(1, 3)
            y = randint(1, 3)
            position = Position(x, y)
            if grid.is_empty(position):
                good_move = True
                grid.set_cell(position, self.cell_state)

    def _complete_line(self, grid: Grid, line: list[Position]):
        play_position = None
        for position in line:
            if grid.is_empty(position):
                play_position = position
                break
        if play_position is not None:
            grid.set_cell(play_position, self.cell_state)

    def medium_move(self, grid):
        # Check if we have a wining move
        winning_pattern = self.get_win_pattern(self.cell_state)
        line = grid.almost_win(winning_pattern)
        if line is not None:
            self._complete_line(grid, line)
        else:
            # Check if we can block the opponent
            adv_state = self.cell_state.get_adversary()
            if adv_state is not None:
                adv_winning_pattern = self.get_win_pattern(adv_state)
                line = grid.almost_win(adv_winning_pattern)
                if line is not None:
                    self._complete_line(grid, line)
                # No winning move and no opponent winning move, make a random move
                else:
                    self.easy_move(grid)

    def hard_move(self, grid: Grid):
        """
            This method is partially generated by the AI-agent.
            The goal of the last step is to use the correct AI-agent to implement the minimax algorithm
            to find the best possible move.
        """
        best_score = float('-inf')
        best_move = None

        for i in range(1, 4):
            for j in range(1, 4):
                position = Position(i, j)
                if grid.is_empty(position):
                    grid.set_cell(position, self.cell_state)
                    score = self._minimax(grid, 0, False)
                    grid.set_cell(position, CellState.EMPTY)

                    if score > best_score:
                        best_score = score
                        best_move = position

        if best_move:
            grid.set_cell(best_move, self.cell_state)

    def _minimax(self, grid: Grid, depth: int, is_maximizing: bool) -> int:
        # Check if game is over
        if grid.is_win(self.cell_state):
            return 1
        if grid.is_win(self.cell_state.get_adversary()):
            return -1
        if all(cell != CellState.EMPTY for cell in grid.linearize()):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(1, 4):
                for j in range(1, 4):
                    position = Position(i, j)
                    if grid.is_empty(position):
                        grid.set_cell(position, self.cell_state)
                        score = self._minimax(grid, depth + 1, False)
                        grid.set_cell(position, CellState.EMPTY)
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(1, 4):
                for j in range(1, 4):
                    position = Position(i, j)
                    if grid.is_empty(position):
                        grid.set_cell(position, self.cell_state.get_adversary())
                        score = self._minimax(grid, depth + 1, True)
                        grid.set_cell(position, CellState.EMPTY)
                        best_score = min(score, best_score)
            return best_score

    def play_move(self, grid: Grid):
        print(f'Making move level "{self._difficulty.value}"')
        match self._difficulty:
            case GameDifficulty.EASY:
                self.easy_move(grid)
            case GameDifficulty.MEDIUM:
                self.medium_move(grid)
            case GameDifficulty.HARD:
                self.hard_move(grid)


class PlayerType(Enum):
    HUMAN = HumanPlayer
    COMPUTER = ComputerPlayer


class Game:

    def __init__(self, player_one: Player, player_two: Player):
        self._grid = Grid()
        self._player_one = player_one
        self._player_two = player_two
        self._current_player = self._player_one

    def is_game_over(self):
        return self._is_grid_full() or self._has_winner()

    def _is_grid_full(self):
        return all(cell != CellState.EMPTY for cell in self._grid.linearize())

    def _has_winner(self):
        return any(self.has_won(player) for player in [self._player_one, self._player_two])

    def get_player(self):
        linear = self._grid.linearize()
        count_X = linear.count(CellState.X)  # 1st player
        count_O = linear.count(CellState.O)  # 2nd player
        if count_X == count_O:
            return CellState.X
        elif count_X > count_O:
            return CellState.O
        else:  # should not occur?
            return CellState.X

    def next_player(self):
        if self._current_player == self._player_one:
            self._current_player = self._player_two
        elif self._current_player == self._player_two:
            self._current_player = self._player_one

    def has_won(self, player: Player):
        return self._grid.is_win(player.cell_state)

    def from_str(self, value: str):
        if len(value) != 9:
            raise ValueError
        valid_values = {state.value for state in CellState}
        if not all(char in valid_values for char in value):
            raise ValueError
        for index in range(len(value)):
            positon = Position(index // 3 + 1, index % 3 + 1)
            self._grid.set_cell(positon, CellState.from_value(value[index]))

    def play(self):
        has_winner = False
        while not self.is_game_over():
            self.display()
            self._current_player.play_move(self._grid)
            if self.has_won(self._current_player):
                self.display()
                print(f"{self._current_player.symbol} wins")
                has_winner = True
            else:
                self.next_player()

        if not has_winner:
            self.display()
            print("Draw")

    def display(self):
        print(self._grid)


class Menu:
    CMD_PLAY = "start"
    CMD_QUIT = "exit"
    MODE_USER = "user"
    MODE_DIFFICULTY = [d.value for d in GameDifficulty]

    def is_param_valid(self, param: str):
        if (param not in Menu.MODE_DIFFICULTY
                and param != Menu.MODE_USER):
            return False
        else:
            return True

    def init_player(self, param: str, symbol: PlayerSymbol):
        if param == Menu.MODE_USER:
            return PlayerType.HUMAN.value(symbol)
        else:
            return PlayerType.COMPUTER.value(GameDifficulty.from_value(param), symbol)

    def create_game(self):
        while True:
            try:
                arg = input("Input command: ").lower().split()
                if len(arg) == 1:
                    if arg[0] == Menu.CMD_QUIT:
                        exit()

                if len(arg) != 3:
                    print("wrong number of parameters:", arg)
                    raise ValueError

                mode, param_player_one, param_player_two = arg
                if mode not in [Menu.CMD_PLAY, Menu.CMD_QUIT]:
                    print("error in mode:", mode)
                    raise ValueError
                if not self.is_param_valid(param_player_one):
                    print("error in player one:", param_player_one)
                    raise ValueError
                if not self.is_param_valid(param_player_two):
                    print("error in player two: ", param_player_two)
                    raise ValueError

                match mode:
                    case Menu.CMD_PLAY:
                        player_one = self.init_player(param_player_one, PlayerSymbol.ONE)
                        player_two = self.init_player(param_player_two, PlayerSymbol.TWO)
                        return Game(player_one, player_two)
                    case Menu.CMD_QUIT:
                        exit()

            except ValueError as e:
                print("Bad Parameters")


if __name__ == "__main__":
    game = Menu().create_game()
    game.play()
