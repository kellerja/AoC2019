from math import sqrt


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
    vec = (end_point[0] - start_point[0], end_point[1] - start_point[1])
    vec_norm = vector_norm(vec)
    return vec[0] / vec_norm, vec[1] / vec_norm


def is_vec_direction_same(unit_vector_a, unit_vector_b, accuracy):
    return abs(unit_vector_a[0] - unit_vector_b[0]) < accuracy and abs(unit_vector_a[1] - unit_vector_b[1]) < accuracy


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
    best_score = 0
    for asteroid in asteroids:
        best_score = max(best_score, count_visible_asteroids_from(asteroid, asteroids))
    write_output(best_score)
    print(best_score)
