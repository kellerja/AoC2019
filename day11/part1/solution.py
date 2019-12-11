from enum import Enum
from computer import read_program, Memory, Process, CPU


class Color(Enum):
    # color = value, draw_symbol
    WHITE = 1, '#'
    BLACK = 0, '.'

    @staticmethod
    def get_from_value(value):
        if value == 1:
            return Color.WHITE
        return Color.BLACK


class Grid:
    def __init__(self):
        self.grid = {
            # coordinate: (color, num_times_visited)
            (0, 0): (Color.BLACK, 0)
        }
        self.top_left = (0, 0)
        self.bottom_right = (0, 0)

    def get_color(self, position):
        return self.grid.get(position, (Color.BLACK, 0))[0]

    def paint(self, position, color):
        self.increase_grid_as_necessary(position)
        self.grid[position] = (color, self.grid.get(position, (Color.BLACK, 0))[1] + 1)

    def increase_grid_as_necessary(self, position):
        self.top_left = (min(self.top_left[0], position[0]), max(self.top_left[1], position[1]))
        self.bottom_right = (max(self.top_left[0], position[0]), min(self.top_left[1], position[1]))


class Direction(Enum):
    # direction = (dx, dy), draw_symbol
    UP = (0, 1), '^'
    DOWN = (0, -1), 'v'
    LEFT = (1, 0), '<'
    RIGHT = (-1, 0), '>'

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
        return self.left_turn()

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


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


if __name__ == '__main__':
    raw_memory = read_program('input.txt')
    robot = Robot(raw_memory)
    cpu = CPU()
    grid = Grid()
    robot.run(cpu, grid)
    write_output(len(grid.grid))
    print(f'At least once colored cell count: {len(grid.grid)}')
