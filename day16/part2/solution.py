def read_input():
    with open('input.txt', 'r') as in_file:
        return [int(digit) for digit in in_file.read().strip()[:]]


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


if __name__ == '__main__':
    current_rot = read_input()
    offset = int(''.join(str(v) for v in current_rot[:7]))
    current_rot = (current_rot * 10_000)[offset:]
    for phase in range(100):
        last_sum = 0
        for idx in range(len(current_rot) - 1, -1, -1):
            last_sum = (last_sum + current_rot[idx]) % 10
            current_rot[idx] = last_sum
    result = ''.join(str(v) for v in current_rot[:8])
    write_output(result)
    print(f'Final value: {result}')
