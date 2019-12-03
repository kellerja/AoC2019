import csv


class CPU:

    def process_addition(self, memory):
        a = memory[memory[self.ic + 1]]
        b = memory[memory[self.ic + 2]]
        memory[memory[self.ic + 3]] = a + b
        self.ic += 3
        return True

    def process_multiply(self, memory):
        a = memory[memory[self.ic + 1]]
        b = memory[memory[self.ic + 2]]
        memory[memory[self.ic + 3]] = a * b
        self.ic += 3
        return True

    def process_halt(self, _):
        return False

    def __init__(self):
        self.ic = 0
        self.OP_CODES = {
            1: self.process_addition,
            2: self.process_multiply,
            99: self.process_halt
        }

    def step(self, memory):
        op = memory[self.ic]
        return self.OP_CODES[op](memory)

    def process(self, memory):
        self.ic = 0
        while self.step(memory):
            self.ic += 1
        return memory


def read_memory():
    mem = []
    with open('input.txt', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            for element in line:
                mem.append(int(element))
    return mem


def write_result(memory):
    result = str(memory[0])
    with open('output.txt', 'w') as file:
        file.write(result)
        file.write('\n')


def pre_process_memory(memory):
    memory[1] = 12
    memory[2] = 2
    return memory


if __name__ == '__main__':
    memory = read_memory()
    memory = pre_process_memory(memory)
    print("Program: " + str(memory))
    cpu = CPU()
    memory = cpu.process(memory)
    print("End state: " + str(memory))
    write_result(memory)
