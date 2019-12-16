def read_input():
    with open('input.txt', 'r') as in_file:
        return [int(digit) for digit in in_file.read().strip()[:]]


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


if __name__ == '__main__':
    current_rot = read_input()
    print(f'Initial value: {"".join(str(v) for v in current_rot)}')
    for phase in range(100):
        new_rot = [None] * len(current_rot)
        for base_index in range(len(current_rot)):
            n = base_index + 1
            val = 0
            for value in range(base_index, len(current_rot), n * 4):
                val += sum(current_rot[value:value+n])
                val -= sum(current_rot[value+2*n:value+3*n])
            new_rot[base_index] = abs(val) % 10
        current_rot = new_rot
    result = ''.join(str(v) for v in current_rot)
    write_output(result[:8])
    print(f'Final value: {result[:8]}')
