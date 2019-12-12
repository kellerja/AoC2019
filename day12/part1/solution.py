import re

VELOCITY_CHANGE_DELTA = 1
AXIS_NUM = 3
SIMULATION_LENGTH = 1000


def apply_gravity(moons):
    for a_idx, moon_a in enumerate(moons):
        for moon_b in moons[a_idx + 1:]:
            for axis in range(AXIS_NUM):
                if moon_a['pos'][axis] < moon_b['pos'][axis]:
                    moon_a['vel'][axis] += VELOCITY_CHANGE_DELTA
                    moon_b['vel'][axis] -= VELOCITY_CHANGE_DELTA
                elif moon_a['pos'][axis] > moon_b['pos'][axis]:
                    moon_a['vel'][axis] -= VELOCITY_CHANGE_DELTA
                    moon_b['vel'][axis] += VELOCITY_CHANGE_DELTA


def apply_velocity(moons):
    for moon in moons:
        for axis in range(AXIS_NUM):
            moon['pos'][axis] += moon['vel'][axis]


def get_debug_string(moon):
    return f"{moon['name']} at {moon['pos']} with vel {moon['vel']}"


def print_step_debug(moons):
    print(f'Time step {time_step}')
    step_total_energy = 0
    for moon in moons:
        print(get_debug_string(moon))
        step_total_energy += get_total_energy(moon)
    print(f'Total energy of the system is {step_total_energy}')
    print()


def get_potential_energy(moon):
    return sum(abs(coord) for coord in moon['pos'])


def get_kinetic_energy(moon):
    return sum(abs(coord) for coord in moon['vel'])


def get_total_energy(moon):
    return get_potential_energy(moon) * get_kinetic_energy(moon)


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
    print_debug = False
    print_debug_step = 100
    for time_step in range(SIMULATION_LENGTH):
        if print_debug and time_step % print_debug_step == 0:
            print_step_debug(moons)
        apply_gravity(moons)
        apply_velocity(moons)
    time_step += 1
    if print_debug and time_step % print_debug_step == 0:
        print_step_debug(moons)
    total_energy = sum(get_total_energy(moon) for moon in moons)
    write_output(total_energy)
    print(f'At the end of the simulation the total energy of the system is {total_energy}')
