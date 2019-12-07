import csv
from itertools import permutations


class Memory:

    def __init__(self, memory):
        self.memory = memory

    def __getitem__(self, item):
        return self.memory[item]

    def __repr__(self):
        return self.memory.__repr__()

    def dereference(self, reference):
        return self.get_value(self.get_value(reference))

    def get_value(self, address):
        return self.memory[address]

    def set_value(self, address, value):
        self.memory[address] = value

    def set_value_by_reference(self, reference, value):
        self.set_value(self.get_value(reference), value)


class IO:

    def __init__(self):
        self.stream = []
        self.inputs = []

    def print(self, value):
        self.stream.append(value)

    def read(self):
        if len(self.inputs) > 0:
            return self.inputs.pop()
        return input()

    def prepare_inputs(self, inputs):
        self.inputs.extend(reversed(inputs))

    def print_entire_output(self):
        print("!!!! OUTPUT !!!!")
        for item in self.stream:
            print(item)
        print("!!!!!!!!!!!!!!!!")


class CPU:

    def get_op(self, memory):
        command = str(memory.get_value(self.ic))
        return int(command[-2:])

    def get_parameter_handlers(self, memory, param_num):
        flags = self.get_parameter_flag(memory)
        if len(flags) >= param_num:
            flag = int(flags[param_num - 1])
            if flag == 1:
                return memory.get_value, memory.set_value
        return memory.dereference, memory.set_value_by_reference

    def get_parameter_flag(self, memory):
        command = str(memory.get_value(self.ic))
        return command[-3::-1]

    def process_addition(self, memory):
        read_1, _ = self.get_parameter_handlers(memory, 1)
        read_2, _ = self.get_parameter_handlers(memory, 2)
        _, write_3 = self.get_parameter_handlers(memory, 3)
        a = read_1(self.ic + 1)
        b = read_2(self.ic + 2)
        write_3(self.ic + 3, a + b)
        self.ic += 3
        return True

    def process_multiply(self, memory):
        read_1, _ = self.get_parameter_handlers(memory, 1)
        read_2, _ = self.get_parameter_handlers(memory, 2)
        _, write_3 = self.get_parameter_handlers(memory, 3)
        a = read_1(self.ic + 1)
        b = read_2(self.ic + 2)
        write_3(self.ic + 3, a * b)
        self.ic += 3
        return True

    def read_input(self, memory):
        value = int(self.io.read())
        _, write_1 = self.get_parameter_handlers(memory, 1)
        write_1(self.ic + 1, value)
        self.ic += 1
        return True

    def print_output(self, memory):
        read_1, _ = self.get_parameter_handlers(memory, 1)
        self.io.print(read_1(self.ic + 1))
        self.ic += 1
        return True

    def jump_if_non_zero(self, memory):
        read_1, _ = self.get_parameter_handlers(memory, 1)
        read_2, _ = self.get_parameter_handlers(memory, 2)
        if read_1(self.ic + 1) != 0:
            self.ic = read_2(self.ic + 2) - 1
        else:
            self.ic += 2
        return True

    def jump_if_zero(self, memory):
        read_1, _ = self.get_parameter_handlers(memory, 1)
        read_2, _ = self.get_parameter_handlers(memory, 2)
        if read_1(self.ic + 1) == 0:
            self.ic = read_2(self.ic + 2) - 1
        else:
            self.ic += 2
        return True

    def less_than(self, memory):
        read_1, _ = self.get_parameter_handlers(memory, 1)
        read_2, _ = self.get_parameter_handlers(memory, 2)
        _, write_3 = self.get_parameter_handlers(memory, 3)
        value = 1 if read_1(self.ic + 1) < read_2(self.ic + 2) else 0
        write_3(self.ic + 3, value)
        self.ic += 3
        return True

    def equals(self, memory):
        read_1, _ = self.get_parameter_handlers(memory, 1)
        read_2, _ = self.get_parameter_handlers(memory, 2)
        _, write_3 = self.get_parameter_handlers(memory, 3)
        value = 1 if read_1(self.ic + 1) == read_2(self.ic + 2) else 0
        write_3(self.ic + 3, value)
        self.ic += 3
        return True

    def process_halt(self, _):
        return False

    def __init__(self):
        self.ic = 0
        self.OP_CODES = {
            1: self.process_addition,
            2: self.process_multiply,
            3: self.read_input,
            4: self.print_output,
            5: self.jump_if_non_zero,
            6: self.jump_if_zero,
            7: self.less_than,
            8: self.equals,
            99: self.process_halt
        }
        self.io = IO()

    def step(self, memory, debug=False):
        op = self.get_op(memory)
        if debug:
            print(f'Starting new step. IC {self.ic} running op {op} ({self.OP_CODES.get(op, lambda x: None).__name__}) with flags {self.get_parameter_flag(memory)} ({memory[self.ic]})')
            print(f'Memory {memory}')
        return self.OP_CODES[op](memory)

    def process(self, memory, debug=False):
        if debug:
            step_count = 0
            print('Starting program\n')
        self.ic = 0
        while self.step(memory, debug):
            self.ic += 1
            if debug:
                step_count += 1
                print(f'Ending step {step_count}')
                print(f'Memory {memory}\n')
        if debug:
            print(f'Ending program. Total steps {step_count}')
            print(f'Memory {memory}')
        return memory


def read_memory():
    mem = []
    with open('input.txt', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            for element in line:
                mem.append(int(element))
    return mem


def write_result(result):
    with open('output.txt', 'w') as file:
        file.write(str(result))
        file.write("\n")


if __name__ == '__main__':
    orig_memory = read_memory()
    print(f'Original program: {orig_memory}')

    highest_signal = 0
    for phase_sequence in permutations(range(0, 5)):
        cpu = CPU()
        cpu.io.stream.append(0)
        for amplifier_phase in phase_sequence:
            cpu.io.prepare_inputs([amplifier_phase, cpu.io.stream[-1]])
            memory = cpu.process(Memory(orig_memory.copy()))
        highest_signal = max(highest_signal, cpu.io.stream[-1])
        print(f'Run complete for sequence {phase_sequence}. Score {cpu.io.stream[-1]}. Input stream length {len(cpu.io.inputs)} output stream length {len(cpu.io.stream)}')
    print(f'Best score {highest_signal}')
    write_result(highest_signal)
