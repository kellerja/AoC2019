from computer import read_program, Memory, Process, CPU, OutputCollector


class Game:
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
        self.score = 0
        self.paddle = []
        self.balls = []

    def add_tile(self, x, y, tile_id):
        tile = self.tiles[tile_id]
        self.board[(x, y)] = tile
        self.right_bottom = (max(self.right_bottom[0], x), max(self.right_bottom[1], y))
        if tile[0] == self.tiles[3][0]:
            self.update_paddle(x, y)
        elif tile[0] == self.tiles[4][0]:
            self.update_balls(x, y)

    def update_paddle(self, x, y):
        self.paddle.append(x)
        for paddle_tile_x in reversed(self.paddle):
            if self.board[(paddle_tile_x, y)][0] != self.tiles[3][0]:
                self.paddle.remove(paddle_tile_x)
        self.paddle.sort()

    def update_balls(self, x, y):
        self.balls.append((x, y))
        for ball in self.balls.copy():
            if self.board[ball][0] != self.tiles[4][0]:
                self.balls.remove(ball)

    def handle_program_output(self, input):
        if input[0] == -1 and input[1] == 0:
            self.score = input[2]
        else:
            self.add_tile(input[0], input[1], input[2])

    def handle_program_input(self):
        closest = (0, 999999999999)
        for ball in self.balls:
            if ball[1] < closest[1]:
                closest = ball
        paddle_middle_x = self.paddle[int(len(self.paddle) / 2)]
        if closest[0] == paddle_middle_x:
            return 0
        elif closest[0] > paddle_middle_x:
            return 1
        return -1


def write_output(result):
    with open('output.txt', 'w') as out_file:
        out_file.write(str(result))
        out_file.write('\n')


if __name__ == '__main__':
    game = Game()
    cpu = CPU()
    memory = Memory(read_program('input.txt'))
    # coins are at mem address 0
    # 2 coins means free play
    memory.memory[0] = 2
    process = Process(memory)
    collector = OutputCollector(3, game.handle_program_output)
    collector.attach(process)
    process.io.wait_input = game.handle_program_input
    cpu.process(process)
    write_output(game.score)
    print(f'Game has finished with score {game.score}')
