from computer import read_program, Memory, Process, CPU, OutputCollector


class Board:
    def __init__(self):
        self.tiles = {
            # tile_id = (name, )
            0: ('empty',),
            1: ('wall',),
            2: ('block',),
            3: ('horizontal paddle',),
            4: ('ball',)
        }
        self.default_tile = self.tiles[0]
        self.board = {}
        # top_left is always (0, 0)
        self.right_bottom = (0, 0)

    def add_tile(self, x, y, tile_id):
        self.board[(x, y)] = self.tiles[tile_id]
        self.right_bottom = (max(self.right_bottom[0], x), max(self.right_bottom[1], y))

    def add_tile_raw(self, input):
        self.add_tile(input[0], input[1], input[2])


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


if __name__ == '__main__':
    board = Board()
    cpu = CPU()
    process = Process(Memory(read_program('input.txt')))
    collector = OutputCollector(3, board.add_tile_raw)
    collector.attach(process)
    cpu.process(process)
    block_tile_count = sum([1 if tile[0] == board.tiles[2][0] else 0 for tile in board.board.values()])
    write_output(block_tile_count)
    print(f'Board has {block_tile_count} block tiles')
