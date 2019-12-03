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

    def get_steps(self):
        return abs(self.end_point.x - self.start_point.x) + abs(self.end_point.y - self.start_point.y)

    def get_steps_to(self, point_on_line):
        return abs(point_on_line.x - self.start_point.x) + abs(point_on_line.y - self.start_point.y)

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


def find_all_intersections(lines_a, lines_b, origin):
    intersections = []
    for lineA in lines_a:
        for lineB in lines_b:
            intersection_point = lineA.intersects(lineB)
            if intersection_point is not None and intersection_point != origin:
                intersections.append(intersection_point)
    return intersections


def find_steps_to_intersection(lines, intersection, limit):
    # print(f"Searching steps for intersection {intersection} on lines {lines} with limit {limit}")
    steps = 0
    for line in lines:
        if steps > limit:
            # print(f"Reached limit {limit} on line {line} with {steps} steps when finding intersection {intersection} on lines {lines}")
            return 99999999999
        if line.is_point_on_line(intersection):
            # print(f"Found intersection {intersection} with steps {line.get_steps_to(intersection)} on line {line} totaling {steps + line.get_steps_to(intersection)} steps on lines {lines}")
            return steps + line.get_steps_to(intersection)
        steps += line.get_steps()
        # print(f"Followed line {line} with steps {line.get_steps()} totaling {steps} steps")
    # print(f"ERROR intersection {intersection} not on lines {lines}")
    return 9999999999


def find_shortest_intersection(lines_a, lines_b, intersections):
    short_a, short_b = 999999999, 9999999999
    short_intersection = None
    for intersection in intersections:
        short_total = short_a + short_b
        steps_a = find_steps_to_intersection(lines_a, intersection, short_total)
        steps_b = find_steps_to_intersection(lines_b, intersection, short_total)
        # print(f"Line A has {steps_a} steps and line B {steps_b} steps to intersection {intersection} totaling {steps_a + steps_b} steps")
        if steps_a + steps_b < short_total:
            short_a = steps_a
            short_b = steps_b
            short_intersection = intersection
    return short_a, short_b, short_intersection


if __name__ == '__main__':
    origin = Point(0, 0)
    raw_lineA, raw_lineB = read_input()
    # raw_lineA = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    # raw_lineB = "U62,R66,U55,R34,D71,R55,D58,R83"
    linesA = to_lines(origin, raw_lineA)
    linesB = to_lines(origin, raw_lineB)
    # print(f"Lines A {linesA}\nLines B {linesB}")
    intersections = find_all_intersections(linesA, linesB, origin)
    steps_a, steps_b, intersection = find_shortest_intersection(linesA, linesB, intersections)

    print(f"Shortest intersection {intersection} with steps line A {steps_a} line B {steps_b} totaling {steps_a + steps_b}")
    write_output(str(steps_a + steps_b))
