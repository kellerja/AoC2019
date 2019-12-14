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
    materials[out_component] -= reaction[0]
    for in_component in reaction[1:]:
        materials[in_component['component']] = materials.get(in_component['component'], 0) + in_component['count']


if __name__ == '__main__':
    reactions = read_input()
    materials = {'FUEL': 1}

    while True:
        current = get_next_required_component(materials)
        if current is None:
            break
        perform_reaction(materials, current, reactions[current])
    write_output(materials['ORE'])
    print(f'To get fuel {materials["ORE"]} ore is required')
