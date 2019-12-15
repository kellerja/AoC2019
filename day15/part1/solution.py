from operator import add
from enum import Enum
from computer import read_program, Memory, Process, CPU, OutputCollector


class MapLegend(Enum):
    # map element = display symbol
    DROID = 'D',
    WALL = '#',
    CLEAR = '.',
    UNKNOWN = ' ',
    OXYGEN_SYSTEM = 'O',


class Direction(Enum):
    # direction = value, delta, opposite_value,
    UP = 1, (0, 1), 2,
    DOWN = 2, (0, -1), 1,
    LEFT = 3, (-1, 0), 4,
    RIGHT = 4, (1, 0), 3,

    @staticmethod
    def get_by_value(value):
        for direction in Direction:
            if direction.value[0] == value:
                return direction


class Area:
    def __init__(self):
        self.map = {
            (0, 0): MapLegend.DROID
        }
        self.top_left = (0, 0)
        self.bottom_right = (0, 0)
        self.oxygen_system = None

    def move_droid(self, droid, direction):
        droid_location = droid.location
        if self.map[droid_location] != MapLegend.DROID:
            raise Exception('Droid location not on map')
        new_droid_location = tuple(map(add, droid_location, direction.value[1]))
        if new_droid_location not in self.map:
            droid.step_count += 1
        else:
            droid.step_count -= 1
        self.map[new_droid_location] = MapLegend.DROID
        droid.location = new_droid_location
        self.map[droid_location] = MapLegend.OXYGEN_SYSTEM if droid_location == self.oxygen_system else MapLegend.CLEAR
        self.reevaluate_map_size(new_droid_location)

    def place_wall(self, droid, direction):
        new_location = tuple(map(add, droid.location, direction.value[1]))
        self.map[new_location] = MapLegend.WALL
        self.reevaluate_map_size(new_location)

    def place_oxygen_system(self, droid):
        self.oxygen_system = droid.location

    def reevaluate_map_size(self, added_pos):
        self.top_left = (min(self.top_left[0], added_pos[0]), max(self.top_left[1], added_pos[1]))
        self.bottom_right = (max(self.bottom_right[0], added_pos[0]), min(self.bottom_right[1], added_pos[1]))

    def get_map_string(self):
        result = ''
        box_size = 2
        height = abs(self.top_left[1] - self.bottom_right[1] + box_size)
        width = abs(self.bottom_right[0] - self.top_left[0] + box_size)
        for y in range(self.bottom_right[1] - box_size, height - abs(self.bottom_right[1]) + 1):
            row = ''
            for x in range(self.top_left[0] - box_size, width - abs(self.top_left[0]) + 1):
                row += self.map.get((x, y), MapLegend.UNKNOWN).value[0]
            result = f'|{row}|\n{result}'
        horizontal_border = '-' * (width + box_size + 2)
        return f'{horizontal_border}\n{result}{horizontal_border}'


def next_location_generator(location, area):
    if area.map.get(location, MapLegend.DROID) != MapLegend.DROID:
        return None
    for direction in Direction:
        new_location = tuple(map(add, location, direction.value[1]))
        if new_location not in area.map:
            yield direction.value[0]
            for move in next_location_generator(new_location, area):
                yield move
            if area.map[new_location] != MapLegend.WALL:
                yield direction.value[2]
    return None


class DroidController:
    def __init__(self, area):
        self.location = (0, 0)
        self.area = area
        self.cpu = CPU()
        self.process = Process(Memory(read_program('input.txt')))
        self.process.io.wait_input = self.provide_input
        self.process.io.listeners = [self.handle_output]
        self.latest_direction = Direction.UP
        self.location_gen = next_location_generator(self.location, self.area)
        self.step_count = 0
        self.oxygen_system_step_count = 0

    def start(self):
        self.cpu.process(self.process)

    def provide_input(self):
        # print(area.get_map_string())
        move = next(self.location_gen, 0)
        self.latest_direction = Direction.get_by_value(move)
        # print(f'Droid is attempting to move {self.latest_direction}')
        return move

    def handle_output(self, value):
        if value == 0:
            area.place_wall(self, self.latest_direction)
        elif value == 1:
            area.move_droid(self, self.latest_direction)
        elif value == 2:
            area.move_droid(self, self.latest_direction)
            area.place_oxygen_system(self)
            self.oxygen_system_step_count = droid.step_count


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


if __name__ == '__main__':
    area = Area()
    droid = DroidController(area)
    droid.start()
    write_output(droid.oxygen_system_step_count)
    print(droid.oxygen_system_step_count)
