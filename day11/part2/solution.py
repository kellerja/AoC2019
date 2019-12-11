from enum import Enum
from computer import read_program, Memory, Process, CPU


class Color(Enum):
    # color = value, draw_symbol, RGB color
    WHITE = 1, '#', (0xff, 0xff, 0xff)
    BLACK = 0, '.', (0x00, 0x00, 0x00)
    UNKNOWN = -1, '?', (0xff, 0x00, 0xff)

    @staticmethod
    def get_from_value(value):
        if value == Color.WHITE.value[0]:
            return Color.WHITE
        elif value == Color.BLACK.value[0]:
            return Color.BLACK
        return Color.UNKNOWN


class Grid:
    def __init__(self):
        self.grid = {
            # coordinate: (color, num_times_visited)
            (0, 0): Color.WHITE
        }
        self.top_left = (0, 0)
        self.bottom_right = (0, 0)

    def get_color(self, position):
        return self.grid.get(position, Color.BLACK)

    def paint(self, position, color):
        self.increase_grid_as_necessary(position)
        self.grid[position] = color

    def increase_grid_as_necessary(self, position):
        self.top_left = (min(self.top_left[0], position[0]), max(self.top_left[1], position[1]))
        self.bottom_right = (max(self.bottom_right[0], position[0]), min(self.bottom_right[1], position[1]))

    def get_color_matrix(self):
        matrix = []
        start_x, len_x = self.top_left[0], self.top_left[0] + abs(self.bottom_right[0] - self.top_left[0])
        start_y, len_y = self.bottom_right[1], self.bottom_right[1] + abs(self.bottom_right[1] - self.top_left[1])
        for y in reversed(range(start_y, len_y + 1)):
            row = []
            for x in range(start_x, len_x + 1):
                row.append(self.grid.get((x, y), Color.BLACK))
            matrix.append(row)
        for x, y in self.grid:
            try:
                matrix[y][x]
            except IndexError:
                print(f'Err: Position {x}, {y} not included in the matrix!!!!!!!!')
        return matrix


class Direction(Enum):
    # direction = (dx, dy), draw_symbol
    UP = (0, 1), '^'
    DOWN = (0, -1), 'v'
    LEFT = (-1, 0), '<'
    RIGHT = (1, 0), '>'

    def left_turn(self):
        if self == Direction.UP:
            return Direction.LEFT
        elif self == Direction.DOWN:
            return Direction.RIGHT
        elif self == Direction.LEFT:
            return Direction.DOWN
        return Direction.UP

    def right_turn(self):
        if self == Direction.UP:
            return Direction.RIGHT
        elif self == Direction.DOWN:
            return Direction.LEFT
        elif self == Direction.LEFT:
            return Direction.UP
        return Direction.DOWN

    def turn(self, amount):
        if amount == 1:
            return self.right_turn()
        elif amount == 0:
            return self.left_turn()
        raise Exception(f'Unknown turn {amount}')

    def move(self, position):
        return position[0] + self.value[0][0], position[1] + self.value[0][1]


class Robot:
    def __init__(self, raw_memory):
        self.position = (0, 0)
        self.direction = Direction.UP
        self.process = Process(Memory(raw_memory))
        self.values = []

    def listen(self, grid, value):
        self.values.append(value)
        if len(self.values) < 2:
            return
        new_color = Color.get_from_value(self.values[0])
        grid.paint(self.position, new_color)
        self.direction = self.direction.turn(self.values[1])
        # print(f'{self.position} is colored to {new_color} and robot moves from {self.position} to ', end='')
        self.move()
        # print(f'{self.position}')
        self.values = []

    def provide_color(self, grid):
        return grid.get_color(self.position).value[0]

    def run(self, cpu, grid):
        self.process.io.wait_input = lambda: self.provide_color(grid)
        self.process.io.listeners = [lambda value: self.listen(grid, value)]
        cpu.process(self.process)

    def move(self):
        self.position = self.direction.move(self.position)


def print_matrix(matrix):
    print('\n'.join(''.join(color.value[1] for color in row) for row in matrix))


def write_output(result, width, height):
    header = f'P6\n{width} {height}\n255\n'
    with open('output.ppm', 'wb') as out_file:
        out_file.write(bytearray(header, 'ascii'))
        out_file.write(bytearray(result))


if __name__ == '__main__':
    raw_memory = read_program('input.txt')
    robot = Robot(raw_memory)
    cpu = CPU()
    grid = Grid()
    robot.run(cpu, grid)
    matrix = grid.get_color_matrix()
    color_array = [color_byte for row in matrix for color in row for color_byte in color.value[2]]
    write_output(color_array, len(matrix[0]), len(matrix))
    print_matrix(matrix)
