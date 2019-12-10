from math import sqrt
from queue import Queue


def read_input():
    asteroids = []
    with open('input.txt', 'r') as in_file:
        for line_nr, line in enumerate(in_file):
            for symbol_idx, symbol in enumerate(line.strip()):
                if symbol == '#':
                    asteroids.append((symbol_idx, line_nr))
    return asteroids


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


def vector_norm(vec):
    return sqrt(pow(vec[0], 2) + pow(vec[1], 2))


def to_unit_vec(start_point, end_point):
    vec = to_vec(start_point, end_point)
    vec_norm = vector_norm(vec)
    return vec[0] / vec_norm, vec[1] / vec_norm


def to_vec(start_point, end_point):
    return end_point[0] - start_point[0], end_point[1] - start_point[1]


def is_vec_direction_same(unit_vector_a, unit_vector_b, accuracy):
    return abs(unit_vector_a[0] - unit_vector_b[0]) < accuracy and abs(unit_vector_a[1] - unit_vector_b[1]) < accuracy


def angle(unit_vec_a, unit_vec_b):
    return (unit_vec_a[0] * unit_vec_b[0] + unit_vec_a[1] + unit_vec_b[1]) / 1


def count_visible_asteroids_from(origin, asteroids):
    not_visible = []
    for target in asteroids:
        if target == origin or target in not_visible:
            continue
        unit_vector_a = to_unit_vec(origin, target)
        for asteroid in asteroids:
            if asteroid == origin or asteroid == target:
                continue
            unit_vector_b = to_unit_vec(origin, asteroid)
            if is_vec_direction_same(unit_vector_a, unit_vector_b, 10e-8):
                not_visible.append(asteroid)
    return len(asteroids) - len(not_visible) - 1


if __name__ == '__main__':
    asteroids = read_input()
    best_score = 286#0
    best_origin = (8,3)#None
    """for asteroid in asteroids:
        score = count_visible_asteroids_from(asteroid, asteroids)
        if score > best_score:
            best_score = score
            best_origin = asteroid"""

    laser_start_unit_vec = to_unit_vec(best_origin, (best_origin[0], best_origin[1] + 1))
    temp_list = []
    for asteroid in asteroids:
        if asteroid == best_origin:
            continue
        vec = to_unit_vec(best_origin, asteroid)
        temp_list.append((round(angle(laser_start_unit_vec, vec), 4), vector_norm(to_vec(best_origin, asteroid)), vec, asteroid))
    queue = Queue()
    for _, _, vec, target in sorted(temp_list, key=lambda x: (x[0], x[1])):
        queue.put((vec, target))

    count = 0
    previous_destroyed_vec = None
    previous_destroyed_target = None
    while not queue.empty() and count < 200:
        vec, target = queue.get()
        if previous_destroyed_vec is not None and is_vec_direction_same(vec, previous_destroyed_vec, 10e-8):
            queue.put((vec, target))
            continue
        previous_destroyed_vec = vec
        previous_destroyed_target = target
        count += 1
        print(f'Destroyed {previous_destroyed_target} with shot {count}')

    result = previous_destroyed_target[0] * 100 + previous_destroyed_target[1]
    write_output(result)
    print(f'{count}th destroyed asteroid is {previous_destroyed_target} that gives a result of {result}')
