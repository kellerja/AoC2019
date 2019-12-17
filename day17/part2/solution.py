from enum import Enum
from queue import Queue

from computer import read_program, Memory, Process, CPU, OutputCollector


class Direction(Enum):
    # direction = value, opposite value, left turn value, right turn value
    LEFT = ord('<'), ord('>'), ord('v'), ord('^')
    RIGHT = ord('>'), ord('<'), ord('^'), ord('v')
    UP = ord('^'), ord('v'), ord('<'), ord('>')
    DOWN = ord('v'), ord('^'), ord('>'), ord('<')

    def get_turn(self, other):
        if self == other:
            return ()
        elif self.value[0] == other.value[1]:
            return ord('L'), ord('L')
        elif other.value[0] == self.value[2]:
            return ord('L'),
        return ord('R'),

    @staticmethod
    def get_required_direction(start, end):
        if start[0] == end[0]:
            return Direction.UP if start[1] - 1 == end[1] else Direction.DOWN
        return Direction.LEFT if start[0] - 1 == end[0] else Direction.RIGHT

    @staticmethod
    def get_by_value(value):
        for direction in Direction:
            if direction.value[0] == value:
                return direction

    @staticmethod
    def get_values():
        return Direction.UP.value[0], Direction.DOWN.value[0], Direction.LEFT.value[0], Direction.RIGHT.value[0]


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


def get_neighbours(x, y, grid):
    path = [ord('#'), *Direction.get_values()]
    if grid[y][x] not in path:
        return False
    neighbours = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        try:
            pos = (x + dx, y + dy)
            if pos[0] < 0 or pos[1] < 0:
                continue
            if grid[pos[1]][pos[0]] in path:
                neighbours.append(pos)
        except IndexError:
            pass
    return neighbours


def is_intersection(neighbours):
    return len(neighbours) >= 3


def is_dead_end(neighbours):
    return len(neighbours) == 1


def is_turn(neighbours):
    return len(neighbours) == 2 and neighbours[0][0] != neighbours[1][0] and neighbours[0][1] != neighbours[1][1]


def find_robot(grid):
    for y, row in enumerate(grid):
        for x, el in enumerate(row):
            if scaffolding[y][x] in Direction.get_values():
                return x, y


def get_paths(grid, pos, direction, reach_string='', visited=[], possible=[]):
    visited.append(pos)
    neighbours = get_neighbours(pos[0], pos[1], grid)
    new_neighbours = 0
    for neighbour in neighbours:
        if neighbour not in visited:
            new_neighbours += 1
            new_reach_string = reach_string
            new_direction = Direction.get_required_direction(pos, neighbour)
            turn = direction.get_turn(new_direction)
            if len(turn) > 0:
                new_reach_string += ''.join(chr(x) for x in turn)
            get_paths(grid, neighbour, new_direction, new_reach_string + '1', visited.copy(), possible)
    if new_neighbours == 0:
        possible.append(reach_string)


class Node:
    def __init__(self, pos, type='UNK'):
        self.type = type
        self.pos = pos
        self.neighbours = []

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos

    def __repr__(self):
        return f'{self.pos}'

    def add_connection(self, node, distance):
        self.neighbours.append((node, distance))

    def has_neighbour(self, other):
        for neighbour, _ in self.neighbours:
            if neighbour == other:
                return True
        return False


def get_graph(start, grid):
    graph = {
        start: []
    }
    queue = Queue()
    start_node = Node(start, 'START')
    discovered = [start]
    parents = [None]
    queue.put((start_node, None, 0))
    while not queue.empty():
        current, parent, count = queue.get()
        neighbours = get_neighbours(current.pos[0], current.pos[1], grid)
        if is_intersection(neighbours):
            graph[current.pos] = current
            current.type = 'INT'
            current.add_connection(parent, count)
            parent.add_connection(current, count)
            parent = current
            count = 0
        elif is_dead_end(neighbours):
            graph[current.pos] = current
            if parent is None:
                parent = current
                count = 0
            else:
                current.type = 'END'
                current.add_connection(parent, count)
                parent.add_connection(current, count)
                count = 0
        elif is_turn(neighbours):
            current.type = 'TURN'
            graph[current.pos] = current
            current.add_connection(parent, count)
            parent.add_connection(current, count)
            parent = current
            count = 0
        for neighbour in neighbours:
            try:
                index = discovered.index(neighbour)
                a = graph[neighbour] if neighbour in graph else parents[index]
                b = current if current.pos in graph else parent
                if a != b:
                    if not a.has_neighbour(b):
                        a.add_connection(b, 99999999)
                    if not b.has_neighbour(a):
                        b.add_connection(a, 99999999)
            except ValueError:
                discovered.append(neighbour)
                parents.append(parent)
                neighbour_node = Node(neighbour)
                queue.put((neighbour_node, parent, count + 1))
    return graph


if __name__ == '__main__':
    scaffolding = []
    cpu = CPU()
    process = Process(Memory(read_program('input.txt')))
    collector = OutputCollector(output_method=OutputCollector.Method.END_INT_EXCLUDE, output_until=10,
                                callback=lambda val: scaffolding.append(val))
    collector.attach(process)
    cpu.process(process)
    print('\n'.join(''.join(chr(x) for x in sub) for sub in scaffolding))

    start = find_robot(scaffolding)
    graph = get_graph(start, scaffolding)
    for key in graph:
        print(f'{key, graph[key].type}={graph[key].neighbours}')

    paths = []
    #get_paths(scaffolding, start, Direction.get_by_value(scaffolding[start[1]][start[0]]), possible=paths)

    write_output(start)
    print(f'Total alignment: {start}')
