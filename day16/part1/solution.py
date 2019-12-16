def read_input():
    with open('input.txt', 'r') as in_file:
        return [int(digit) for digit in in_file.read().strip()[:]]


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')

def get(base, idx):
    if base == 0 and idx == 0:
        return 1
    elif base == 0:
        return 0
    base += 1
    base_pattern = [0, 1, 0, -1]
    capped_idx = idx % base * len(base_pattern)
    return base_pattern[int(capped_idx / base)]


def get_multiplier(base_index):
    base_pattern = [0, 1, 0, -1]
    for idx, value in enumerate(base_pattern):
        repeating = base_index + 1
        if idx == 0:
            repeating -= 1
        for repeating in range(repeating):
            yield value
    while True:
        for value in base_pattern:
            for repeating in range(base_index + 1):
                yield value


if __name__ == '__main__':
    current_rot = read_input()
    print(f'Initial value: {"".join(str(v) for v in current_rot)}')
    for phase in range(100):
        new_rot = [None] * len(current_rot)
        for base_index in range(len(current_rot)):
            new_value = 0
            multiplier = get_multiplier(base_index)
            for idx, value in enumerate(current_rot):
                new_value += get(base_index, idx) * value
            new_rot[base_index] = abs(new_value) % 10
        current_rot = new_rot
    result = ''.join(str(v) for v in current_rot)
    write_output(result[:8])
    print(f'Final value: {result[:8]}')
