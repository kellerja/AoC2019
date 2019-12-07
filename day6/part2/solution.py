def read_input():
    with open('input.txt', 'r') as in_file:
        return in_file.readlines()


def write_result(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


def count_edges_between(graph, start_node, end_node, count=0, best=9999999999999, visited=[]):
    if start_node == end_node:
        return count
    if count > best:
        return count
    visited.append(start_node)
    for child in graph.get(start_node, []):
        if child in visited:
            continue
        best = min(best, count_edges_between(graph, child, end_node, count + 1, best, visited))
    return best


if __name__ == '__main__':
    orbits = {
    }
    for orbit in read_input():
        object_and_satellite = orbit.strip().split(')')
        orbits.setdefault(object_and_satellite[0], set()).add(object_and_satellite[1])
        orbits.setdefault(object_and_satellite[1], set()).add(object_and_satellite[0])
    start = orbits['YOU'].pop()
    end = orbits['SAN'].pop()
    count = count_edges_between(orbits, start, end)
    write_result(count)
