from math import gcd
from functools import reduce
import copy
import re


def lcm(a, b):
    return int(abs(a * b) / gcd(a, b))


def list_lcm(multiples):
    return reduce(lcm, multiples)


def simulate_step(moons, axis):
    for a_idx, moon_a in enumerate(moons):
        for moon_b in moons[a_idx + 1:]:
            if moon_a['pos'][axis] < moon_b['pos'][axis]:
                moon_a['vel'][axis] += 1
                moon_b['vel'][axis] -= 1
            elif moon_a['pos'][axis] > moon_b['pos'][axis]:
                moon_a['vel'][axis] -= 1
                moon_b['vel'][axis] += 1
        moon_a['pos'][axis] += moon_a['vel'][axis]


def read_input():
    coordinates = []
    line_regex = '<x=(?P<x>.*), y=(?P<y>.*), z=(?P<z>.*)>'
    pattern = re.compile(line_regex)
    with open('input.txt', 'r') as in_file:
        for line in in_file:
            matches = pattern.match(line)
            coordinates.append([
                int(matches.group('x')),
                int(matches.group('y')),
                int(matches.group('z'))
            ])
    return coordinates


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


def get_initial_moons():
    moons = [
        {
            'name': 'Io',
            'pos': [-1, 0, 2],
            'vel': [0, 0, 0]
        },
        {
            'name': 'Europa',
            'pos': [2, -10, -7],
            'vel': [0, 0, 0]
        },
        {
            'name': 'Ganymede',
            'pos': [4, -8, 8],
            'vel': [0, 0, 0]
        },
        {
            'name': 'Callisto',
            'pos': [3, 5, -1],
            'vel': [0, 0, 0]
        },
    ]
    initial_coords = read_input()
    for idx in range(len(moons)):
        moons[idx]['pos'] = initial_coords[idx]
    return moons


if __name__ == '__main__':
    moons = get_initial_moons()
    initial_state = copy.deepcopy(moons)
    results = []
    for axis in range(3):
        time_step = 0
        state_match_found = False
        while not state_match_found:
            simulate_step(moons, axis)
            all_moons_vel_zero = True
            for idx, moon in enumerate(moons):
                if 0 != moon['vel'][axis] or initial_state[idx]['pos'][axis] != moon['pos'][axis]:
                    all_moons_vel_zero = False
            state_match_found = all_moons_vel_zero
            time_step += 1
        results.append(time_step)
    write_output(list_lcm(results))
    print(f'Equal universe state discovered at step {list_lcm(results)}')
