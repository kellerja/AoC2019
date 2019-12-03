def direction_to_y_multiplier(direction):
    if direction == 'U':
        return 1
    elif direction == 'D':
        return -1
    return 0


def direction_to_x_multiplier(direction):
    if direction == 'R':
        return 1
    elif direction == 'L':
        return -1
    return 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction, amount):
        new_x = self.x + direction_to_x_multiplier(direction) * amount
        new_y = self.y + direction_to_y_multiplier(direction) * amount
        return Point(new_x, new_y)

    def manhattan_distance(self, other_point):
        return max(self.x, other_point.x) - min(self.x, other_point.x)\
               + max(self.y, other_point.y) - min(self.y, other_point.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.x},{self.y})"


class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.x_direction = start_point.y == end_point.y

    def get_min_x(self):
        return min(self.start_point.x, self.end_point.x)

    def get_max_x(self):
        return max(self.start_point.x, self.end_point.x)

    def get_min_y(self):
        return min(self.start_point.y, self.end_point.y)

    def get_max_y(self):
        return max(self.start_point.y, self.end_point.y)

    def is_point_on_line(self, point):
        if self.x_direction:
            return point.y == self.start_point.y and self.get_min_x() <= point.x <= self.get_max_x()
        return point.x == self.start_point.x and self.get_min_y() <= point.y <= self.get_max_y()

    def intersects(self, other_line):
        if self.x_direction == other_line.x_direction:
            return None
        intersection_x = min(self.get_max_x(), other_line.get_max_x())
        intersection_y = min(self.get_max_y(), other_line.get_max_y())
        possible_intersection = Point(intersection_x, intersection_y)
        debug_str = (f"Possible intersection {possible_intersection} "
                     f"is on {self}? {self.is_point_on_line(possible_intersection)} "
                     f"and on {other_line}? {other_line.is_point_on_line(possible_intersection)}")
        # print(debug_str)
        if self.is_point_on_line(possible_intersection) and other_line.is_point_on_line(possible_intersection):
            return possible_intersection
        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"[({self.start_point})->({self.end_point})]"


def to_lines(origin, raw_input):
    lines = []
    current_point = origin
    for step in raw_input.split(','):
        direction = step[0]
        amount = int(step[1:])
        new_point = current_point.move(direction, amount)
        lines.append(Line(current_point, new_point))
        current_point = new_point
    return lines


def read_input():
    with open('input.txt', 'r') as input_file:
        raw_a = input_file.readline().strip()
        raw_b = input_file.readline().strip()
    return raw_a, raw_b


def write_output(result):
    with open('output.txt', 'w') as output_file:
        output_file.write(result)
        output_file.write('\n')


if __name__ == '__main__':
    origin = Point(0, 0)
    raw_lineA, raw_lineB = read_input()
    linesA = to_lines(origin, raw_lineA)
    linesB = to_lines(origin, raw_lineB)

    # print(f"Lines A {linesA}\nLines B {linesB}")

    shortest_intersection = None
    shortest_intersection_dist = 999999999999
    for lineA in linesA:
        for lineB in linesB:
            intersection_point = lineA.intersects(lineB)
            if intersection_point is not None and intersection_point != origin:
                distance = origin.manhattan_distance(intersection_point)
                # print(f"Found intersection {intersection_point} between {lineA} and {lineB} with distance {distance} from origin")
                if distance <= shortest_intersection_dist:
                    shortest_intersection_dist = distance
                    shortest_intersection = intersection_point
    print(f"Closest intersection {shortest_intersection} with distance {shortest_intersection_dist}")
    write_output(str(shortest_intersection_dist))
