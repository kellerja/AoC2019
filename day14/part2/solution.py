from math import ceil, floor


def read_input():
    reactions = {}
    with open('input.txt', 'r') as in_file:
        for line in in_file:
            bases, result = line.strip().split('=>')
            result_count, result_component = result.strip().split()
            reaction = [int(result_count)]
            for base in bases.strip().split(','):
                count, component = base.strip().split()
                reaction.append({
                    'component': component,
                    'count': int(count)
                })
            reactions[result_component] = reaction
    return reactions


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


def get_next_required_component(materials):
    for material in materials:
        if materials[material] > 0 and material != 'ORE':
            return material
    return None


def perform_reaction(materials, out_component, reaction):
    num_of_reactions = ceil(materials[out_component] / reaction[0])
    materials[out_component] -= reaction[0] * num_of_reactions
    for in_component in reaction[1:]:
        materials[in_component['component']] = materials.get(in_component['component'], 0) + in_component['count'] * num_of_reactions


def get_ore_for(reactions, fuel):
    materials = {'FUEL': fuel}
    while True:
        current = get_next_required_component(materials)
        if current is None:
            break
        perform_reaction(materials, current, reactions[current])
    return materials['ORE']


def binary_search(reactions):
    total_ore = 1_000_000_000_000
    low = 1
    high = 1_000_000_000_000
    mid = None
    while low <= high:
        mid = floor(low + high) // 2
        ores = get_ore_for(reactions, mid)
        if ores < total_ore:
            low = mid + 1
        elif ores > total_ore:
            high = mid - 1
        else:
            return mid
    return mid


if __name__ == '__main__':
    reactions = read_input()
    total_fuel = binary_search(reactions)
    write_output(total_fuel)
    print(f'To get {total_fuel} fuel {1000000000000} ore is required')
