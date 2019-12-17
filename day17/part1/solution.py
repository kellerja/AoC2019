from computer import read_program, Memory, Process, CPU, OutputCollector


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


def is_intersection(x, y, grid):
    if grid[y][x] != 35:
        return False
    total_neighbours = 0
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        try:
            if grid[y + dy][x + dx] == 35:
                total_neighbours += 1
        except IndexError:
            pass
    return total_neighbours >= 3


if __name__ == '__main__':
    scaffolding = []
    cpu = CPU()
    process = Process(Memory(read_program('input.txt')))
    collector = OutputCollector(output_method=OutputCollector.Method.END_INT_EXCLUDE, output_until=10,
                                callback=lambda val: scaffolding.append(val))
    collector.attach(process)
    cpu.process(process)
    print('\n'.join(''.join(chr(x) for x in sub) for sub in scaffolding))

    total_alignment_parameter = 0
    for y, row in enumerate(scaffolding):
        for x, el in enumerate(row):
            if is_intersection(x, y, scaffolding):
                total_alignment_parameter += x * y
    write_output(total_alignment_parameter)
    print(f'Total alignment: {total_alignment_parameter}')
