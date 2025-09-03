from dataclasses import dataclass
from enum import Enum


class DimensionsException(Exception):
    pass


class CellVisitedException(Exception):
    pass


@dataclass
class Config:
    BOARD_WIDTH: int
    BOARD_HEIGHT: int
    CELL_SIZE: int = None
    MODE: str = None

    def __post_init__(self):
        if self.BOARD_WIDTH < 0 or self.BOARD_HEIGHT < 0:
            raise DimensionsException()
        self.CELL_SIZE = len(str(self.BOARD_WIDTH * self.BOARD_HEIGHT))


class Position:
    """
    Represents a position on a game board.

    :ivar config: The Config object contains board configurations
    :type config: Config
    """

    def __init__(self, x: int, y: int, config: Config):
        if (not x in range(1, config.BOARD_WIDTH + 1)
                or not y in range(1, config.BOARD_HEIGHT + 1)):
            raise DimensionsException()
        self.config = config
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_index(self) -> tuple[int, int]:
        """
        Convert board coordinates to array indices.

        :return: A tuple of (row_index, column_index)
        :rtype: tuple[int, int]
        """
        return self.config.BOARD_HEIGHT - self._y, self._x - 1

    def __add__(self, other):
        return Position(self._x + other.x, self._y + other.y, self.config)

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __hash__(self):
        return hash((self._x, self._y))

    def __str__(self):
        return f'({self._x}, {self._y})'


class Knight:
    """
    Represents a Knight piece in a chess-like game and handles its behavior.

    :var MOVES: List of possible moves for the knight.
    :type MOVES: list[tuple[int, int]]
    :ivar config: Configuration object defining the constraints and rules of the game.
    :type config: Config
    """
    MOVES: list[tuple[int, int]] = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             (1, -2), (1, 2), (2, -1), (2, 1)]

    def __init__(self, position: Position, config: Config):
        self.config = config
        self._position = position

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position


class CellState(Enum):
    VOID = "_"
    KNIGHT = "X"
    VISITED = "*"


class Cell:
    """
    Represents a cell in a grid or similar structure.

    :ivar state: Current state of the cell. It can either be an integer or an
        instance of CellState.
    :type state: CellState | int
    """

    def __init__(self, state: CellState | int = CellState.VOID, size: int = 2):
        self._state = state
        self._size = size

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: CellState | int):
        self._state = state

    def is_void(self):
        return self.state == CellState.VOID

    def __str__(self):
        cell_list = [" " if not self.is_void() else "_"] * self._size
        if not self.is_void():
            if isinstance(self._state, CellState):
                cell_list[-1] = self._state.value
            else:
                if self._state > 9:
                    cell_list[-1] = str(self._state % 10)
                    cell_list[-2] = str(self._state // 10)
                else:
                    cell_list[-1] = str(self._state)
        return "".join(cell_list)


class Board:
    """
    Representation of a board for a game involving the chess piece knight.

    :ivar board: Two-dimensional list representing the board, where each element
                 is an instance of Cell.
    :type board: list[list[Cell]]
    """

    def __init__(self, config: Config, knight: Knight):
        self._config = config
        self.board = [[Cell(size=config.CELL_SIZE)
                       for _ in range(config.BOARD_WIDTH)] for _ in range(config.BOARD_HEIGHT)]
        self._knight = knight
        self.possible_moves = []

    def reset (self):
        self.board = [[Cell(size=self._config.CELL_SIZE)
                       for _ in range(self._config.BOARD_WIDTH)] for _ in range(self._config.BOARD_HEIGHT)]

    def is_game_over(self):
        return len(self.possible_moves) == 0

    def full_board_visited(self):
        for row in self.board:
            for cell in row:
                if cell.state == CellState.VOID:
                    return False
        return True

    def count_visited(self):
        count = 0
        for row in self.board:
            for cell in row:
                if cell.state in (CellState.VISITED, CellState.KNIGHT):
                    count += 1
        return count

    def is_cell_void(self, position: Position):
        i, j = position.get_index()
        return self.board[i][j].is_void()

    def set_cell_state(self, position: Position, state: CellState | int):
        i, j = position.get_index()
        self.board[i][j].state = state

    def update_knight(self):
        self.set_cell_state(self._knight.position, CellState.KNIGHT)
        self.possible_moves = self.get_all_possible_moves(self._knight.position)
        self.set_knight_move()

    def set_knight_move(self):
        for pos in self.possible_moves:
            self.set_cell_state(pos, len(self.get_all_possible_moves(pos)))

    def move_knight(self, new_position: Position):
        if new_position in self.possible_moves:
            for pos in self.possible_moves:
                self.set_cell_state(pos, CellState.VOID)

            self.set_cell_state(self._knight.position, CellState.VISITED)
            self._knight.position = new_position
            self.update_knight()
        else:
            raise CellVisitedException()
            print("Invalid move!" ,end=" ")

    def get_all_possible_moves(self, position: Position):
        return [
            Position(position.x + dx, position.y + dy, self._config)
            for dx, dy in Knight.MOVES
            if self._is_valid_move(position.x + dx, position.y + dy)
        ]

    def _is_valid_move(self, x: int, y: int):
        try:
            new_position = Position(x, y, self._config)
            return self.is_cell_void(new_position)
        except (DimensionsException, CellVisitedException):
            return False

    def __str__(self):
        line_delimiter = "-" * (self._config.BOARD_WIDTH * (self._config.CELL_SIZE + 1) + 3)
        border_str = " " * (self._config.CELL_SIZE - 1) + line_delimiter + "\n"
        for i in range(self._config.BOARD_HEIGHT):
            line = [str(cell) for cell in self.board[i]]
            border_str += (str(self._config.BOARD_HEIGHT - i).rjust(self._config.CELL_SIZE - 1)
                           + "| " + ' '.join(line) + " |\n")
        border_str += " " * (self._config.CELL_SIZE - 1) + line_delimiter + "\n"

        border_str += " " * (self._config.CELL_SIZE + 1) + ' '.join(
            [str(i).rjust(self._config.CELL_SIZE) for i in range(1, self._config.BOARD_WIDTH + 1)]) + "\n"
        return border_str


class Game:

    def __init__(self, config: Config, starting_position: Position):
        self._config = config
        self._knight = Knight(starting_position, config)
        self._board = Board(config, self._knight)
        self.solvable = self.resolve(starting_position)
        self.solution = ""
        if self.solvable:
            self.solution = str(self._board)
            self._board.reset()
            if config.MODE == "PUZZLE":
                self._board.update_knight()
                print(self._board)

    def display(self):
        print(self._board)

    def play(self):
        while not self._board.full_board_visited():
            #print(f"hint: optimal {self.get_optimal_move()}")
            x, y = input("Enter your next move: ").split()
            try:
                new_position = Position(int(x), int(y), self._config)
                self._board.move_knight(new_position)
            except (DimensionsException, CellVisitedException):
                print("Invalid move!", end=" ")
            else:
                print(self._board)
                if self._board.is_game_over():
                    print("No more possible moves !")
                    print(f"Your knight visited {self._board.count_visited()} squares!")
                    break
        if self._board.full_board_visited():
            print("What a great tour! Congratulations!")

    def resolve(self, current_position, index=0):
        self._board.set_cell_state(current_position, index + 1)

        if self._board.full_board_visited():
            return True
        else:
            list_move = self._board.get_all_possible_moves(current_position)
            for move in list_move:
                if self.resolve(move, index + 1):
                    return True
            self._board.set_cell_state(current_position, CellState.VOID)
            return False


def valid_input(entry: str) -> tuple[int, int]:
    args = entry.split()
    if len(args) != 2:
        raise DimensionsException()
    val_1, val_2 = map(int, args)
    if val_1 < 1 or val_2 < 1:
        raise DimensionsException()
    return val_1, val_2


def ask_input(prompt: str, creator_func, error_message: str):
    while True:
        try:
            entry = input(prompt)
            x, y = valid_input(entry)
            result = creator_func(x, y)
        except (DimensionsException, ValueError):
            print(error_message)
        else:
            return result


def ask_config() -> Config:
    return ask_input(
        prompt="Enter your board dimensions: ",
        creator_func=lambda x, y: Config(x, y),
        error_message="Invalid Dimension!"
    )


def ask_position(config: Config) -> Position:
    return ask_input(
        prompt="Enter the knight's starting position: ",
        creator_func=lambda x, y: Position(x, y, config),
        error_message="Invalid position!"
    )

def ask_mode(config: Config):
    while True:
        mode = input("Do you want to try the puzzle? (y/n) ").lower()
        if mode == "y":
            config.MODE = "PUZZLE"
            return config
        elif mode == "n":
            config.MODE = "RESOLVE"
            return config
        else:
            print("Invalid input!")


if __name__ == '__main__':
    config = ask_config()
    position = ask_position(config)
    config = ask_mode(config)
    game = Game(config, position)

    if game.solvable:
        if config.MODE == "PUZZLE":
            game.play()
        elif config.MODE == "RESOLVE":
            print("Here is the solution!")
            print(game.solution)
    else:
        print(f"No solution exists!")
