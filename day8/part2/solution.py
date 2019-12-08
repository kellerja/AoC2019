from enum import Enum


def read_input():
    with open('input.txt' , 'r') as in_file:
        return ''.join(in_file.readlines())


def write_output(result, width, height):
    header = f'P6\n{width} {height}\n255\n'
    with open('output.ppm', 'wb') as out_file:
        out_file.write(bytearray(header, 'ascii'))
        out_file.write(bytearray(result))


class Colors(Enum):
    BLACK = '0', (0x00, 0x00, 0x00),
    WHITE = '1', (0xff, 0xff, 0xff),
    TRANSPARENT = '2', (0xff, 0x00, 0xff)


if __name__ == '__main__':
    width, height = (25, 6)
    layer_size = width * height
    raw_input = read_input()
    final_image = [Colors.TRANSPARENT] * layer_size
    for layer_number in range(int(len(raw_input) / layer_size)):
        layer_start_idx = layer_number * layer_size
        layer = raw_input[layer_start_idx:layer_start_idx + layer_size]
        for index, color in enumerate(final_image):
            if color == Colors.TRANSPARENT:
                for color_enum in Colors:
                    if color_enum.value[0] == layer[index]:
                        final_image[index] = color_enum

    write_output([color_byte for color in final_image for color_byte in color.value[1]], width, height)
    final_image_text_layer = [color.value[0] for color in final_image]
    final_image_text = '\n'.join([''.join(final_image_text_layer[i * width:i * width + width]) for i in range(int(len(final_image_text_layer) / width))])
    print(final_image_text)
