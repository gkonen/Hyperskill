# Write your code here
from enum import Enum
from abc import ABC, abstractmethod


class TetrominoName(Enum):
    O = "O"
    I = "I"
    S = "S"
    Z = "Z"
    L = "L"
    J = "J"
    T = "T"


class Tetrominos(ABC):
    """
    Represents a generic Tetromino piece in a Tetris-like game.

    This is an abstract base class designed to define the structure and behavior of
    Tetromino pieces.

    :ivar name: The name of the Tetromino.
    :type name: TetrominoName
    :ivar new_line: The boundary value for wrapping positions.
    :type new_line: int
    :ivar rotation: The current rotation state of the Tetromino.
    :type rotation: int
    """

    def __init__(self, name: TetrominoName, new_line: int):
        self.name = name
        self.new_line = new_line
        self.state_list = []
        self.rotation = 0

    @property
    def state(self):
        return self.state_list[self.rotation]

    def next_rotate(self):
        new_rotation = (self.rotation + 1) % len(self.state_list)
        return self.state_list[new_rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.state_list)

    def state_to_left(self, state):
        return [val - 1 if (val - 1) % self.new_line != (self.new_line - 1)
                else (val - 1 + self.new_line) for val in state]

    def move_left(self):
        new_state = []
        for state in self.state_list:
            new_state.append(self.state_to_left(state))
        self.state_list = new_state

    def state_to_right(self, state):
        return [val + 1 if (val + 1) % self.new_line != 0
                else (val + 1 - self.new_line) for val in state]

    def move_right(self):
        new_state = []
        for state in self.state_list:
            new_state.append(self.state_to_right(state))
        self.state_list = new_state

    def state_to_down(self, state):
        return [val + self.new_line for val in state]

    def move_down(self):
        new_state = []
        for state in self.state_list:
            new_state.append(self.state_to_down(state))
        self.state_list = new_state

    @abstractmethod
    def construct(self, position):
        pass


# region Tetromino class
class Tetro_O(Tetrominos):

    def __init__(self, new_line: int, position: int):
        super().__init__(TetrominoName.O, new_line)
        self.construct(position)

    def construct(self, position):
        self.state_list = [[position, position + 1,
                            position + self.new_line, position + self.new_line + 1]]


class Tetro_I(Tetrominos):

    def __init__(self, new_line: int, position: int):
        super().__init__(TetrominoName.I, new_line)
        self.construct(position)

    def construct(self, position):
        self.state_list = []
        self.state_list.append([position + i * self.new_line for i in range(4)])
        self.state_list.append([position + i for i in range(-1, 3)])


class Tetro_S(Tetrominos):

    def __init__(self, new_line: int, position: int):
        super().__init__(TetrominoName.S, new_line)
        self.construct(position)

    def construct(self, position):
        self.state_list = []
        self.state_list.append([position, position + 1,
                                position + self.new_line - 1, position + self.new_line])
        self.state_list.append([position, position + self.new_line,
                                position + self.new_line + 1, position + 2 * self.new_line + 1])


class Tetro_Z(Tetrominos):

    def __init__(self, new_line: int, position: int):
        super().__init__(TetrominoName.Z, new_line)
        self.construct(position)

    def construct(self, position):
        self.state_list = []
        self.state_list.append([position, position + 1,
                                position + self.new_line + 1, position + self.new_line + 2])
        self.state_list.append([position, position + self.new_line - 1,
                                position + self.new_line, position + 2 * self.new_line - 1])


class Tetro_L(Tetrominos):

    def __init__(self, new_line: int, position: int):
        super().__init__(TetrominoName.L, new_line)
        self.construct(position)

    def construct(self, position):
        self.state_list = []
        self.state_list.append([position, position + self.new_line,
                                position + 2 * self.new_line, position + 2 * self.new_line + 1])
        self.state_list.append([position + 1, position + self.new_line - 1,
                                position + self.new_line, position + self.new_line + 1])
        self.state_list.append([position, position + 1,
                                position + self.new_line + 1, position + 2 * self.new_line + 1])
        self.state_list.append([position + self.new_line - 1, position + self.new_line,
                                position + self.new_line + 1, position + 2 * self.new_line - 1])


class Tetro_J(Tetrominos):

    def __init__(self, new_line: int, position: int):
        super().__init__(TetrominoName.J, new_line)
        self.construct(position)

    def construct(self, position):
        self.state_list = []
        self.state_list.append([position + 1, position + self.new_line + 1,
                                position + 2 * self.new_line + 1, position + 2 * self.new_line])
        self.state_list.append([position - 1, position,
                                position + 1, position + self.new_line + 1])
        self.state_list.append([position, position + 1,
                                position + self.new_line, position + 2 * self.new_line])
        self.state_list.append([position, position + self.new_line,
                                position + self.new_line + 1, position + self.new_line + 2])


class Tetro_T(Tetrominos):

    def __init__(self, new_line: int, position: int):
        super().__init__(TetrominoName.T, new_line)
        self.construct(position)

    def construct(self, position):
        self.state_list = []
        self.state_list.append([position, position + self.new_line,
                                position + self.new_line + 1, position + 2 * self.new_line])
        self.state_list.append([position, position + self.new_line - 1,
                                position + self.new_line, position + self.new_line + 1])
        self.state_list.append([position + 1, position + self.new_line,
                                position + self.new_line + 1, position + 2 * self.new_line + 1])
        self.state_list.append([position, position + 1,
                                position + 2, position + self.new_line + 1])


class TetroBuilder:
    """
    Responsible for constructing Tetromino objects based on the specified type.

    Static Methods:
        - build: Constructs and returns a Tetromino object based on the given name.
    """

    @staticmethod
    def build(name: TetrominoName, new_line: int, position: int):
        tetro = None
        match name:
            case TetrominoName.O:
                tetro = Tetro_O(new_line, position)
            case TetrominoName.I:
                tetro = Tetro_I(new_line, position)
            case TetrominoName.S:
                tetro = Tetro_S(new_line, position)
            case TetrominoName.Z:
                tetro = Tetro_Z(new_line, position)
            case TetrominoName.L:
                tetro = Tetro_L(new_line, position)
            case TetrominoName.J:
                tetro = Tetro_J(new_line, position)
            case TetrominoName.T:
                tetro = Tetro_T(new_line, position)
        return tetro


# endregion

class Grid:
    """
    Represents a grid for a Tetris-like game.

    This class is responsible for managing the grid where Tetromino pieces are
    placed, moved, and combined during gameplay.

    :ivar height: The height of the grid.
    :type height: int
    :ivar width: The width of the grid.
    :type width: int
    :var piece: The current Tetromino piece placed or moving on the grid.
    :type piece: Tetrominos
    :var grid: The grid of the game.
    :type grid: list[list[str]]
    """
    CASE_FREE = "-"
    CASE_TOKEN = "0"

    def __init__(self, height: int = 20, width: int = 10):
        self._height = height
        self._width = width
        self._piece = None
        self._grid = [["-" for _ in range(width)] for _ in range(height)]

    @property
    def width(self):
        return self._width

    @property
    def piece(self):
        return self._piece

    def get_value(self, line, column):
        return line * self._width + column

    def get_index(self, value):
        return value // self._width, value % self._width

    def is_on_left_frontier(self):
        state = self._piece.state
        return any(map(lambda s: s % self._width == 0, state))

    def is_on_right_frontier(self):
        state = self._piece.state
        return any(map(lambda s: s % self._width == self._width - 1, state))

    def is_on_floor(self):
        state = self._piece.state
        return any(map(lambda s: (self._height - 1) * self._width <= s, state))

    def is_game_over(self):
        return any(map(lambda case: case == Grid.CASE_TOKEN, self._grid[0]))

    def break_line(self):
        last_line = self._grid[-1]
        if all(map(lambda case: case == Grid.CASE_TOKEN, last_line)):
            self._grid.pop()
            self._grid.insert(0, [Grid.CASE_FREE for _ in range(self._width)])
            self.break_line()

    def state_valid(self, state: list[int]):
        for val in state:
            line, column = self.get_index(val)
            if self._grid[line][column] == Grid.CASE_TOKEN:
                return False
        return True

    def update_cell(self, state: list[int], value):
        for index in state:
            line, column = self.get_index(index)
            self._grid[line][column] = value

    def place(self, tetro: Tetrominos):
        self._piece = tetro
        self.update_cell(tetro.state, Grid.CASE_TOKEN)

    def action(self, new_state, func):
        if not self.is_on_floor():
            self.update_cell(self._piece.state, Grid.CASE_FREE)
            if self.state_valid(new_state):
                func()
                self.update_cell(self._piece.state, Grid.CASE_TOKEN)
            else:
                self.update_cell(self._piece.state, Grid.CASE_TOKEN)

    def rotate(self):
        state_rotate = self._piece.next_rotate()
        self.action(state_rotate, self._piece.rotate)

    def left(self):
        state_left = self._piece.state_to_left(self._piece.state)
        if not self.is_on_left_frontier():
            self.action(state_left, self._piece.move_left)

    def right(self):
        state_right = self._piece.state_to_right(self._piece.state)
        if not self.is_on_right_frontier():
            self.action(state_right, self._piece.move_right)

    def down(self):
        state_down = self._piece.state_to_down(self._piece.state)
        self.action(state_down, self._piece.move_down)

    def __str__(self):
        message = ""
        for i in range(self._height):
            message += " ".join(self._grid[i]) + "\n"
        return message


class Game:
    """
    Represents a game, responsible for managing the game's grid, receiving user input,
    and executing the game logic.

    :ivar grid: The grid where the game pieces are placed and the game is played.
    :type grid: Grid
    """

    def __init__(self, width: int, height: int):
        self.grid = Grid(height=height, width=width)

    def _new_piece_command(self) -> bool:
        bloc = input()
        name = TetrominoName(bloc)
        tetro = TetroBuilder.build(name, self.grid.width, (self.grid.width - 1) // 2)
        self.grid.place(tetro)
        return False

    def _execute_command(self, command: str, static: bool) -> bool:
        if static:
            if command == "piece":
                return self._new_piece_command()
            elif command == "break":
                self.grid.break_line()
            return static

        match command:
            case "rotate":
                self.grid.rotate()
                self.grid.down()
            case "down":
                self.grid.down()
            case "left":
                self.grid.left()
                self.grid.down()
            case "right":
                self.grid.right()
                self.grid.down()
        return static

    def _get_command(self) -> str:
        command_list = ["rotate", "down", "left", "right", "exit", "piece", "break"]
        while True:
            try:
                cmd = input("")
                if cmd in command_list:
                    return cmd
                raise ValueError
            except ValueError:
                print("Invalid command, try again")

    def play(self):
        static = True
        end_game = False
        while not end_game:
            print(self.grid)
            command = self._get_command()
            if command == "exit":
                break

            old_state = self.grid.piece.state if self.grid.piece else []
            static = self._execute_command(command, static)
            new_state = self.grid.piece.state if self.grid.piece else []

            if old_state and all([old == new for old, new in zip(old_state, new_state)]):
                static = True
                if self.grid.is_game_over():
                    print(self.grid)
                    print("Game Over!")
                    end_game = True


if __name__ == "__main__":
    width, height = input("").split()
    game = Game(int(width), int(height))
    game.play()
