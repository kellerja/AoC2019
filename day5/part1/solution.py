import csv


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
        self.inputs.extend(inputs)

    def print_entire_output(self):
        print("!!!! OUTPUT !!!!")
        for item in self.stream:
            print(item)
        print("!!!!!!!!!!!!!!!!")


class CPU:
    R1 = 0

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

    def process_halt(self, _):
        return False

    def __init__(self):
        self.ic = 0
        self.OP_CODES = {
            1: self.process_addition,
            2: self.process_multiply,
            3: self.read_input,
            4: self.print_output,
            99: self.process_halt
        }
        self.io = IO()

    def step(self, memory, debug=False):
        op = self.get_op(memory)
        if debug:
            print(f'Starting new step. IC {self.ic} running op {op}')
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
    print("Original program: " + str(orig_memory))
    cpu = CPU()
    cpu.io.prepare_inputs([1])
    memory = cpu.process(Memory(orig_memory))
    print("End state: " + str(memory))
    cpu.io.print_entire_output()
    write_result(cpu.io.stream.pop())
