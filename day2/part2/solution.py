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


def write_result(noun, verb):
    result = 100 * noun + verb
    with open('output.txt', 'w') as file:
        file.write(str(result))
        file.write("\n")


def pre_process_memory(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb
    return memory


def find_noun_and_verb_that_results_in(expected_result):
    for noun in range(100):
        for verb in range(100):
            memory = orig_memory.copy()
            memory = pre_process_memory(memory, noun, verb)
            cpu = CPU()
            memory = cpu.process(memory)
            if expected_result == memory[0]:
                return noun, verb, memory


if __name__ == '__main__':
    orig_memory = read_memory()
    print("Original program: " + str(orig_memory))
    noun, verb, memory = find_noun_and_verb_that_results_in(19690720)
    print("End state: " + str(memory))
    write_result(noun, verb)
