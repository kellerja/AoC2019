def read_input():
    with open('input.txt' , 'r') as in_file:
        return ''.join(in_file.readlines())


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


if __name__ == '__main__':
    layer_size = 25 * 6
    raw_input = read_input()
    fewest_zeroes = 999999999
    matching_layer = ''
    for layer_number in range(0, int(len(raw_input) / layer_size)):
        layer_start_idx = layer_number * layer_size
        layer = raw_input[layer_start_idx:layer_start_idx + layer_size]
        zeroes = layer.count('0')
        if zeroes < fewest_zeroes:
            fewest_zeroes = zeroes
            matching_layer = layer
    write_output(matching_layer.count('1') * matching_layer.count('2'))
    print(matching_layer.count('1') * matching_layer.count('2'))
