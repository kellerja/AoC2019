def read_input():
    with open('input.txt', 'r') as in_file:
        return in_file.readlines()


def write_result(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


def count_edges(graph, node, count=0):
    if node in graph:
        count += 1 + count_edges(graph, graph[node])
    return count


if __name__ == '__main__':
    direct_orbits = {
    }
    for orbit in read_input():
        object_and_satellite = orbit.strip().split(')')
        direct_orbits[object_and_satellite[1]] = object_and_satellite[0]
    count = 0
    for satellite in direct_orbits.keys():
        count += count_edges(direct_orbits, satellite)
    write_result(count)
